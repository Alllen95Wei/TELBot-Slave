import asyncio
from machine import Pin, UART

from comms import UARTCommunicator
from constants import GeneralConstants
from subsystems import Chassis, Conveyor, Shooter

# ==============================================================================
# Hardware Initialization
# ==============================================================================
uart = UART(
    1,
    baudrate=GeneralConstants.UART.BAUD_RATE,
    tx=Pin(GeneralConstants.UART.TX_PIN),
    rx=Pin(GeneralConstants.UART.RX_PIN),
    rxbuf=512,
)

# Onboard LED for status indication (Pico W uses "LED", regular Pico uses GP25)
try:
    led = Pin("LED", Pin.OUT)
except Exception:
    try:
        led = Pin(25, Pin.OUT)
    except Exception:
        led = None

# ==============================================================================
# Subsystems Initialization
# ==============================================================================
m_chassis = Chassis()
m_shooter = Shooter()
m_conveyor = Conveyor()

# ==============================================================================
# Communicator Setup
# ==============================================================================
comm = UARTCommunicator(
    uart=uart,
    m_chassis=m_chassis,
    m_shooter=m_shooter,
    m_conveyor=m_conveyor,
    watchdog_timeout_ms=400,
    led_pin=led,
)


async def main():
    print("TELBot Pico W firmware starting...")
    await comm.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down motors...")
        comm.stop_all()
