from subsystems import SubsystemBase
from controllers import GeneralPWM, SparkMAX
from constants import ShooterConstants
from utils import clamp

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
            ShooterConstants.AngleAdj.CLK_PIN,
            ShooterConstants.AngleAdj.EN_PIN,
            ShooterConstants.AngleAdj.REVERSED
        )

        self.motors = {self.upper_flywheel, self.lower_flywheel, self.angle_adj}

    def start_shoot(self, speed: float):
        speed = clamp(speed)
        self.upper_flywheel.set_speed(speed)
        self.lower_flywheel.set_speed(speed)

    def stop_shoot(self):
        self.upper_flywheel.stop()
        self.lower_flywheel.stop()

    def set_angle_speed(self, speed: float):
        speed = clamp(speed)
        self.angle_adj.set_speed(speed)

    def stop_angle(self):
        self.angle_adj.stop()

    def stop_all(self):
        self.upper_flywheel.stop()
        self.lower_flywheel.stop()
        self.angle_adj.stop()   
