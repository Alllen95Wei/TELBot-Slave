from subsystems import SubsystemBase
from controllers import GeneralPWM, SparkMAX
from constants import ConveyorConstants

class Conveyor(SubsystemBase):
    def __init__(self) -> None:
        self.spinner = GeneralPWM(
            ConveyorConstants.Spinner.PWM_PIN,
            reversed=ConveyorConstants.Spinner.REVERSED,
            freq=50,
            use_duty_cycle=False,
            min_pulse_width=1300,
            max_pulse_width=1700
        )
        self.trigger = SparkMAX(
            ConveyorConstants.Trigger.PWM_PIN,
            reversed=ConveyorConstants.Trigger.REVERSED
        )

        self.motors = {self.spinner, self.trigger}

    def start_spinner(self, reversed: bool = False):
        self.spinner.set_speed(1 if not reversed else -1)

    def stop_spinner(self):
        self.spinner.stop()

    def start_trigger(self, speed: float):
        speed = min(1, max(-1, speed))
        self.trigger.set_speed(speed)

    def stop_trigger(self):
        self.trigger.stop()

    def stop_all(self):
        self.spinner.stop()
        self.trigger.stop()
