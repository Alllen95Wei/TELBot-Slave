from subsystems import SubsystemBase
from controllers import SparkMAX, TB6560
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
        self.angle_adj = TB6560(
            ShooterConstants.AngleAdj.CW_PIN,
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

    def start_angle(self, reverse: bool = False):
        self.angle_adj.start(reverse)

    def stop_angle(self):
        self.angle_adj.stop()

    def stop_all(self):
        self.upper_flywheel.stop()
        self.lower_flywheel.stop()
        self.angle_adj.stop()   
