import asyncio
import time
from machine import UART
from subsystems import Chassis, Shooter, Conveyor

try:
    import ustruct as struct
except ImportError:
    import struct

# Compatibility fallbacks for desktop unit testing
if not hasattr(time, "ticks_ms"):
    time.ticks_ms = lambda: int(time.time() * 1000)
if not hasattr(time, "ticks_diff"):
    time.ticks_diff = lambda a, b: a - b

from comms.parser import PacketParser
from comms.protocol import (
    CMD_ACK,
    CMD_PING,
    CMD_RUN,
    CMD_STOP,
    CMD_TELEMETRY,
    PART_ALL,
    PART_CHASSIS,
    PART_CONVEYOR,
    PART_SENSORS,
    PART_SHOOTER,
    Packet,
)


class UARTCommunicator:
    """
    MicroPython UART Communicator for TELBot Pico W.
    Handles real-time binary packet reception, frame decoding, deadman watchdog,
    and sensor telemetry broadcast over UART.
    """

    def __init__(
        self,
        uart,
        m_chassis=None,
        m_shooter=None,
        m_conveyor=None,
        watchdog_timeout_ms: int = 400,
        led_pin=None,
    ) -> None:
        self.uart: UART = uart
        self.chassis: Chassis | None = m_chassis
        self.shooter: Shooter | None = m_shooter
        self.conveyor: Conveyor | None = m_conveyor

        self.watchdog_timeout_ms = watchdog_timeout_ms
        self.led = led_pin

        self.parser = PacketParser()
        self._last_cmd_ticks = time.ticks_ms()
        self._is_stopped = False
        self._running = False
        self._tx_seq = 0

    def send_packet(self, cmd: int, part: int, payload: bytes = b"", seq: int = 0) -> None:
        """Encodes and writes a binary packet to UART."""
        pkt = Packet(cmd=cmd, part=part, payload=payload, seq=seq)
        self.uart.write(pkt.encode())

    def stop_all(self) -> None:
        """Safety stop across all connected subsystems."""
        if self.chassis is not None:
            self.chassis.stop_all()
        if self.shooter is not None:
            self.shooter.stop_all()
        if self.conveyor is not None:
            self.conveyor.stop_all()
        if self.led is not None:
            try:
                self.led.off()
            except Exception:
                pass
        self._is_stopped = True

    def dispatch_packet(self, pkt: Packet) -> None:
        """Dispatches validated packets to appropriate robot subsystems."""
        # 1. Emergency or normal STOP
        if pkt.cmd == CMD_STOP:
            if pkt.part == PART_ALL:
                self.stop_all()
            elif pkt.part == PART_CHASSIS and self.chassis:
                self.chassis.stop_all()
            elif pkt.part == PART_SHOOTER and self.shooter:
                self.shooter.stop_all()
            elif pkt.part == PART_CONVEYOR and self.conveyor:
                self.conveyor.stop_all()
            return

        # 2. Heartbeat PING -> Reply with ACK
        if pkt.cmd == CMD_PING:
            self.send_packet(CMD_ACK, PART_ALL, seq=pkt.seq)
            return

        # 3. RUN Commands
        if pkt.cmd == CMD_RUN:
            # --- Chassis Drive ---
            if pkt.part == PART_CHASSIS and self.chassis:
                if len(pkt.payload) == 6:
                    vx, vy, omega = struct.unpack("<hhh", pkt.payload)
                    self.chassis.drive(vx / 1000.0, omega / 1000.0, vy / 1000.0)

            # --- Shooter Subsystem ---
            elif pkt.part == PART_SHOOTER and self.shooter:
                if len(pkt.payload) == 4:
                    flywheel, start_angle, reverse_angle = struct.unpack("<hBB", pkt.payload)
                    self.shooter.start_shoot(flywheel / 1000.0)
                    if start_angle:
                        self.shooter.start_angle(bool(reverse_angle))
                    else:
                        self.shooter.stop_angle()
                elif len(pkt.payload) == 3:
                    _, start_angle, reverse_angle = struct.unpack("<BBB", pkt.payload)
                    if start_angle:
                        self.shooter.start_angle(bool(reverse_angle))
                    else:
                        self.shooter.stop_angle()
                elif len(pkt.payload) == 2:
                    (flywheel,) = struct.unpack("<h", pkt.payload)
                    self.shooter.start_shoot(flywheel / 1000.0)
                elif len(pkt.payload) == 1:
                    self.shooter.disable_angle()

            # --- Conveyor Subsystem ---
            elif pkt.part == PART_CONVEYOR and self.conveyor:
                if len(pkt.payload) == 4:
                    trigger, spinner_run, spinner_rev = struct.unpack("<hBB", pkt.payload)
                    self.conveyor.start_trigger(trigger / 1000.0)
                    if spinner_run:
                        self.conveyor.start_spinner(reversed=bool(spinner_rev))
                    else:
                        self.conveyor.stop_spinner()
                elif len(pkt.payload) == 3:
                    _, spinner_run, spinner_rev = struct.unpack("<BBB", pkt.payload)
                    if spinner_run:
                        self.conveyor.start_spinner(reversed=bool(spinner_rev))
                    else:
                        self.conveyor.stop_spinner()
                elif len(pkt.payload) == 2:
                    (trigger,) = struct.unpack("<h", pkt.payload)
                    self.conveyor.start_trigger(trigger / 1000.0)

    # ==========================================================================
    # Async Background Tasks
    # ==========================================================================
    async def rx_task(self) -> None:
        """Reads and parses incoming UART packets continuously."""
        while self._running:
            if self.uart.any():
                chunk = self.uart.read()
                if chunk:
                    packets = self.parser.feed(chunk)
                    for pkt in packets:
                        self._last_cmd_ticks = time.ticks_ms()
                        self._is_stopped = False
                        if self.led:
                            self.led.toggle()
                        self.dispatch_packet(pkt)

            # Yield control to allow motor PWM and other coroutines to run smoothly
            await asyncio.sleep_ms(2)

    async def watchdog_task(self) -> None:
        """Safety deadman monitor: stops robot if UART connection drops."""
        while self._running:
            elapsed = time.ticks_diff(time.ticks_ms(), self._last_cmd_ticks)
            if elapsed > self.watchdog_timeout_ms and not self._is_stopped:
                self.stop_all()
            await asyncio.sleep_ms(50)

    async def telemetry_task(self) -> None:
        """Broadcasts sensor telemetry to Host at 20 Hz (every 50 ms)."""
        while self._running:
            # Construct telemetry frame (<HhhB: battery_mv, enc_lf, enc_rf, status_flags)
            # Future sensor readings (ADC, I2C, encoders) can be hooked in here
            battery_mv = 12400  # Default nominal 12.4V
            enc_lf = 0
            enc_rf = 0
            status_flags = 0x01 if not self._is_stopped else 0x00

            payload = struct.pack("<HhhB", battery_mv, enc_lf, enc_rf, status_flags)
            self.send_packet(CMD_TELEMETRY, PART_SENSORS, payload=payload, seq=self._tx_seq)
            self._tx_seq = (self._tx_seq + 1) & 0xFF

            await asyncio.sleep_ms(50)

    async def run(self) -> None:
        """Starts all concurrent tasks and runs until cancelled."""
        self._running = True
        self.stop_all()

        t_rx = asyncio.create_task(self.rx_task())
        t_wd = asyncio.create_task(self.watchdog_task())
        t_telem = asyncio.create_task(self.telemetry_task())

        try:
            await asyncio.gather(t_rx, t_wd, t_telem)
        finally:
            self._running = False
            self.stop_all()
            t_rx.cancel()
            t_wd.cancel()
            t_telem.cancel()
            await asyncio.gather(t_rx, t_wd, t_telem, return_exceptions=True)
