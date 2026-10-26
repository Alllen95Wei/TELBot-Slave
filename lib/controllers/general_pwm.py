from machine import Pin, PWM
from micropython import const

from controllers import ControllerBase

_U16_MAX = const(65535)

class GeneralPWM(ControllerBase):
    def __init__(
            self, 
            pin: int,
            reversed: bool = False,
            freq: int = 1000,
            use_duty_cycle: bool = True,
            min_pulse_width: int | None = None,
            max_pulse_width: int | None = None,
        ) -> None:
        self.pin = PWM(Pin(pin, Pin.OUT), freq=freq)
        self.reversed = reversed
        
        if not use_duty_cycle and (min_pulse_width == None or max_pulse_width == None):
            raise TypeError("`min_pulse_width` and `max_pulse_width` should be set when `use_duty_cycle` is `False`.")
    
        if isinstance(min_pulse_width, int) and isinstance(max_pulse_width, int):
            self.use_duty_cycle = use_duty_cycle
            self.zero_pw = (min_pulse_width + max_pulse_width) / 2
            self.range_pw = max_pulse_width - min_pulse_width

    def set_speed(self, speed: float):
        if speed < -1 or speed > 1:
            raise ValueError("`speed` must be between -1 and 1")
        speed *= (-1 if self.reversed else 1)
        if self.use_duty_cycle:
            duty = int(abs(speed) * _U16_MAX)
            self.pin.duty_u16(duty)
        else:
            duty = self.zero_pw + self.range_pw * speed
            self.pin.duty_ns(int(duty * 1000))

    def stop(self):
        if self.use_duty_cycle:
            self.pin.duty_u16(0)
        else:
            self.pin.duty_ns(int(self.zero_pw * 1000))
