from machine import Pin, PWM
from micropython import const
from time import ticks_us, ticks_diff

from controllers import ControllerBase

_U16_HALF = const(32768)


class TB6560(ControllerBase):
    def __init__(
            self, 
            cw_pin: int, 
            clk_pin: int, 
            en_pin: int, 
            reversed: bool = False,
            freq: int = 200
        ):
        self.freq = freq

        self.cw_pin = Pin(cw_pin, mode=Pin.OUT)
        self.clk_pin = PWM(Pin(clk_pin), freq=freq)
        self.en_pin = Pin(en_pin, mode=Pin.OUT)
        self.reversed = reversed

        self.is_running: bool = False
        self.is_reversed: bool = False
        self.last_start_time: int | None = None
        self.last_end_time: int | None = None
        self.step_count: int = 0

        self.disable()

    def enable(self):
        if self.is_enabled():
            return
        # stop clock before enabling for safety
        self.stop()
        self.en_pin.off()

    def disable(self):
        self.stop()
        self.en_pin.on()

    def is_enabled(self) -> bool:
        return self.en_pin.value() == 0

    def start(self, reverse: bool = False):
        reverse = bool(reverse)
        if self.is_running:
            if self.is_reversed == reverse:
                return
            # Commit steps accumulated in the previous direction before reversing
            self.is_running = False
            self.last_end_time = ticks_us()
            self.get_step()

        self.enable()
        self.is_running = True
        # xor
        self.cw_pin.value(bool(reverse) != bool(self.reversed))
        self.clk_pin.duty_u16(_U16_HALF)
        self.last_start_time = ticks_us()
        self.is_reversed = reverse

    def stop(self):
        self.clk_pin.duty_u16(0)
        if not self.is_running:
            return
        self.is_running = False
        self.last_end_time = ticks_us()
        self.get_step()

    def get_step(self) -> int:
        if self.last_start_time is None:
            return self.step_count
        if self.is_running:
            end_time = ticks_us()
        else:
            end_time = self.last_end_time
        steps = int((ticks_diff(end_time, self.last_start_time) / 10**6 * self.freq) * \
                    (-1 if self.is_reversed else 1))
        if not self.is_running:
            self.step_count += steps
            self.last_start_time = None
            return self.step_count
        else:
            return self.step_count + steps
