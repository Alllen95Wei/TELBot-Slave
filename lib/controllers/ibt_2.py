from machine import Pin, PWM
from micropython import const

_U16_MAX = const(65535)

class IBT_2:
    def __init__(self, l_en_pin: int, r_en_pin: int, l_pwm_pin: int, r_pwm_pin: int, reversed: bool = False, freq: int = 1000):
        self.l_en_pin = Pin(l_en_pin, Pin.OUT)
        self.r_en_pin = Pin(r_en_pin, Pin.OUT)
        self.l_pwm_pin = PWM(Pin(l_pwm_pin), freq=freq)
        self.r_pwm_pin = PWM(Pin(r_pwm_pin), freq=freq)
        self.reversed = reversed

    def enable(self):
        # Set PWM to 0 before enabling for safety
        self.l_pwm_pin.duty_u16(0)
        self.r_pwm_pin.duty_u16(0)
        self.l_en_pin.on()
        self.r_en_pin.on()

    def disable(self):
        self.l_en_pin.off()
        self.r_en_pin.off()
        self.l_pwm_pin.duty_u16(0)
        self.r_pwm_pin.duty_u16(0)

    def is_enabled(self) -> bool:
        return self.l_en_pin.value() == 1 and self.r_en_pin.value() == 1

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
