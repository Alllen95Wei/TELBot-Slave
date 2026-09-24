from controllers import IBT_2
from constants import ChassisConstants

class Chassis:
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
        if not (-1 <= y_speed <= 1) or not (-1 <= z_rotation <= 1) or not (-1 <= x_speed <= 1):
            raise ValueError("inputs must be between -1 and 1")
        lf_speed = y_speed + z_rotation + x_speed
        lr_speed = y_speed + z_rotation + x_speed
        rf_speed = y_speed - z_rotation - x_speed
        rr_speed = y_speed - z_rotation - x_speed

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