from machine import Pin, PWM
from micropython import const

from controllers import ControllerBase

_U16_MAX = const(65535)

class IBT_2(ControllerBase):
    def __init__(
            self, 
            l_en_pin: int | None, 
            r_en_pin: int | None, 
            l_pwm_pin: int, 
            r_pwm_pin: int, 
            reversed: bool = False, 
            freq: int = 1000
        ):
        self.l_en_pin = Pin(l_en_pin, Pin.OUT) if l_en_pin is not None else None
        self.r_en_pin = Pin(r_en_pin, Pin.OUT) if r_en_pin is not None else None
        self.l_pwm_pin = PWM(Pin(l_pwm_pin), freq=freq)
        self.r_pwm_pin = PWM(Pin(r_pwm_pin), freq=freq)
        self.reversed = reversed

        self.stop()

    def enable(self):
        # Set PWM to 0 before enabling for safety
        self.l_pwm_pin.duty_u16(0)
        self.r_pwm_pin.duty_u16(0)
        if self.l_en_pin is not None:
            self.l_en_pin.on()
        if self.r_en_pin is not None:
            self.r_en_pin.on()

    def disable(self):
        if self.l_en_pin is not None:
            self.l_en_pin.off()
        if self.r_en_pin is not None:
            self.r_en_pin.off()
        self.l_pwm_pin.duty_u16(0)
        self.r_pwm_pin.duty_u16(0)

    def is_enabled(self) -> bool:
        l_en = True
        r_en = True
        if self.l_en_pin is not None:
            l_en = bool(self.l_en_pin.value())
        if self.r_en_pin is not None:
            r_en = bool(self.r_en_pin.value())
        return l_en and r_en

    def set_speed(self, speed: float):
        if speed < -1 or speed > 1:
            raise ValueError("`speed` must be between -1 and 1")
        duty = int(abs(speed) * _U16_MAX)
        if (speed * (-1 if self.reversed else 1)) > 0:
            self.l_pwm_pin.duty_u16(duty)
            self.r_pwm_pin.duty_u16(0)
        else:
            self.l_pwm_pin.duty_u16(0)
            self.r_pwm_pin.duty_u16(duty)

    def stop(self):
        self.set_speed(0)
