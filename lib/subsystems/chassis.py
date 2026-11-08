from controllers import IBT_2
from constants import ChassisConstants
from subsystems import SubsystemBase
from utils import clamp

class Chassis(SubsystemBase):
    def __init__(self):
        self.left_front = IBT_2(
            ChassisConstants.LeftFront.L_EN_PIN, 
            ChassisConstants.LeftFront.R_EN_PIN, 
            ChassisConstants.LeftFront.L_PWM_PIN, 
            ChassisConstants.LeftFront.R_PWM_PIN,
            ChassisConstants.LeftFront.REVERSED
        )
        self.left_rear = IBT_2(
            ChassisConstants.LeftRear.L_EN_PIN, 
            ChassisConstants.LeftRear.R_EN_PIN, 
            ChassisConstants.LeftRear.L_PWM_PIN, 
            ChassisConstants.LeftRear.R_PWM_PIN,
            ChassisConstants.LeftRear.REVERSED
        )
        self.right_front = IBT_2(
            ChassisConstants.RightFront.L_EN_PIN, 
            ChassisConstants.RightFront.R_EN_PIN, 
            ChassisConstants.RightFront.L_PWM_PIN, 
            ChassisConstants.RightFront.R_PWM_PIN,
            ChassisConstants.RightFront.REVERSED
        )
        self.right_rear = IBT_2(
            ChassisConstants.RightRear.L_EN_PIN, 
            ChassisConstants.RightRear.R_EN_PIN, 
            ChassisConstants.RightRear.L_PWM_PIN, 
            ChassisConstants.RightRear.R_PWM_PIN,
            ChassisConstants.RightRear.REVERSED
        )

        self.motors = {self.left_front, self.left_rear, self.right_front, self.right_rear}

    def enable(self):
        self.left_front.enable()
        self.left_rear.enable()
        self.right_front.enable()
        self.right_rear.enable()

    def disable(self):
        self.left_front.disable()
        self.left_rear.disable()
        self.right_front.disable()
        self.right_rear.disable()

    def drive(self, y_speed: float, z_rotation: float, x_speed: float = 0):
        y_speed = clamp(y_speed)
        z_rotation = clamp(z_rotation)
        x_speed = clamp(x_speed)

        # 1. Coordinate Transformation:
        # The robot's front is rotated 90 deg clockwise relative to the chassis frame.
        # Moving forward (+y_robot) requires moving right (+x_chassis).
        # Strafing right (+x_robot) requires moving backward (-y_chassis).
        y_c = -x_speed
        x_c = y_speed

        # 2. Mecanum Kinematics for Standard X-configuration:
        # Looking top-down, the ground contact force vectors form an "X" pointing to the center:
        #   LF (1): +45 deg force vector (forward + right)
        #   RF (2): -45 deg force vector (forward + left)
        #   LR (3): -45 deg force vector (forward + left)
        #   RR (4): +45 deg force vector (forward + right)
        # Kinematics equations:
        #   lf = y + x + z
        #   lr = y - x + z
        #   rf = y - x - z
        #   rr = y + x - z
        lf_speed = y_c + x_c + z_rotation
        lr_speed = y_c - x_c + z_rotation
        rf_speed = y_c - x_c - z_rotation
        rr_speed = y_c + x_c - z_rotation

        max_speed = max(abs(lf_speed), abs(lr_speed), abs(rf_speed), abs(rr_speed))
        if max_speed > 1:
            lf_speed /= max_speed
            lr_speed /= max_speed
            rf_speed /= max_speed
            rr_speed /= max_speed

        self.left_front.set_speed(lf_speed)
        self.left_rear.set_speed(lr_speed)
        self.right_front.set_speed(rf_speed)
        self.right_rear.set_speed(rr_speed)