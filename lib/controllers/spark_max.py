from controllers import GeneralPWM

class SparkMAX(GeneralPWM):
    def __init__(self, pin: int, reversed: bool = False) -> None:
        super().__init__(
            pin, 
            reversed, 
            freq=100, 
            use_duty_cycle=False, 
            min_pulse_width=1000, 
            max_pulse_width=2000,
        )
