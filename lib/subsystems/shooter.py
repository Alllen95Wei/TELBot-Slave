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

        self.motors = {self.upper_flywheel, self.lower_flywheel, self.angle_adj}

    def start_shoot(self, speed: float):
        speed = min(1, max(-1, speed))
        self.upper_flywheel.set_speed(speed)
        self.lower_flywheel.set_speed(speed)

    def stop_shoot(self):
        self.upper_flywheel.stop()
        self.lower_flywheel.stop()

    def stop_all(self):
        self.upper_flywheel.stop()
        self.lower_flywheel.stop()
        self.angle_adj.stop()   
