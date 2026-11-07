from machine import Pin, PWM

from controllers import ControllerBase

_U16_HALF = const(32768)


class TB6560(ControllerBase):
    def __init__(self, cw_pin: int, clk_pin: int, en_pin: int, reversed: bool = False):
        self.cw_pin = Pin(cw_pin, mode=Pin.OUT)
        self.clk_pin = PWM(Pin(clk_pin), freq=10)
        self.en_pin = Pin(en_pin, mode=Pin.OUT)
        self.reversed = reversed

        self.cw_pin.off()

    def enable(self):
        # stop clock before enabling for safety
        self.cw_pin.off()
        self.en_pin.on()

    def disable(self):
        self.en_pin.off()

    def is_enabled(self) -> bool:
        return self.en_pin.value() == 1

    def start(self, reverse: bool = False):
        # xor
        self.cw_pin.value(bool(reverse) != bool(self.reversed))
        self.clk_pin.duty_u16(_U16_HALF)

    def stop(self):
        self.clk_pin.duty_u16(0)
