from subsystems import SubsystemBase
from controllers import GeneralPWM, SparkMAX
from constants import ShooterConstants

class Shooter(SubsystemBase):
    def __init__(self) -> None:
        self.upper_flywheel = SparkMAX(
            ShooterConstants.UpperFlywheel.PWM_PIN,
            ShooterConstants.UpperFlywheel.REVERSED
        )
        self.lower_flywheel = SparkMAX(
            ShooterConstants.LowerFlywheel.PWM_PIN,
            ShooterConstants.LowerFlywheel.REVERSED
        )
        self.angle_adj = GeneralPWM(
            ShooterConstants.AngleAdj.PWM_PIN,
            ShooterConstants.AngleAdj.REVERSED
        )
        self.spinner = GeneralPWM(
            ShooterConstants.Spinner.PWM_PIN,
            freq=50,
            use_duty_cycle=False,
            min_pulse_width=1300,
            max_pulse_width=1700
        )

        self.motors = {self.upper_flywheel, self.lower_flywheel, self.angle_adj, self.spinner}

    def start_shoot(self, speed: float):
        speed = min(1, max(-1, speed))
        self.upper_flywheel.set_speed(speed)
        self.lower_flywheel.set_speed(speed)

    def stop_shoot(self):
        self.upper_flywheel.stop()
        self.lower_flywheel.stop()

    def spin_forward(self):
        self.spinner.set_speed(1)
    
    def spin_backward(self):
        self.spinner.set_speed(-1)

    def stop_spin(self):
        self.spinner.stop()

    def stop_all(self):
        self.upper_flywheel.stop()
        self.lower_flywheel.stop()
        self.angle_adj.stop()
        self.spinner.stop()    
