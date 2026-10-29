__all__ = ["GeneralConstants", "ChassisConstants"]

class GeneralConstants:
    class UART:
        BAUD_RATE = 115200
        TX_PIN = 4
        RX_PIN = 5

class ChassisConstants:
    class LeftFront:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 21
        R_PWM_PIN = 20
        REVERSED = False

    class LeftRear:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 10
        R_PWM_PIN = 11
        REVERSED = False

    class RightFront:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 19
        R_PWM_PIN = 18
        REVERSED = True

    class RightRear:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 12
        R_PWM_PIN = 13
        REVERSED = True

class ShooterConstants:
    class UpperFlywheel:
        PWM_PIN = 0
        REVERSED = False

    class LowerFlywheel:
        PWM_PIN = 0
        REVERSED = True

    class AngleAdj:
        PWM_PIN = 0
        REVERSED = False

    class Spinner:
        PWM_PIN = 0
        REVERSED = False
