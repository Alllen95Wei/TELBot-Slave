__all__ = ["GeneralConstants", "ChassisConstants", "ShooterConstants", "ConveyorConstants"]

class GeneralConstants:
    class UART:
        BAUD_RATE = 115200
        ID = 0
        TX_PIN = 16
        RX_PIN = 17

class ChassisConstants:
    class LeftFront:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 9
        R_PWM_PIN = 8
        REVERSED = False

    class LeftRear:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 7
        R_PWM_PIN = 6
        REVERSED = False

    class RightFront:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 5
        R_PWM_PIN = 4
        REVERSED = True

    class RightRear:
        L_EN_PIN = 0
        R_EN_PIN = 0
        L_PWM_PIN = 3
        R_PWM_PIN = 2
        REVERSED = True

class ShooterConstants:
    class UpperFlywheel:
        PWM_PIN = 19
        REVERSED = False

    class LowerFlywheel:
        PWM_PIN = 18
        REVERSED = True

    class AngleAdj:
        CW_PIN = 10
        CLK_PIN = 11
        EN_PIN = 12
        REVERSED = False

class ConveyorConstants:
    class Spinner:
        PWM_PIN = 21
        REVERSED = False

    class Trigger:
        PWM_PIN = 20
        REVERSED = False
    
