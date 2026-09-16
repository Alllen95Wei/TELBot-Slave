__all__ = ["GeneralConstants", "ChassisConstants", "ShooterConstants", "ConveyorConstants"]

class GeneralConstants:
    class UART:
        BAUD_RATE = 115200
        ID = 0
        TX_PIN = 16
        RX_PIN = 17

class ChassisConstants:
    class LeftFront:
        L_EN_PIN = None
        R_EN_PIN = None
        L_PWM_PIN = 7
        R_PWM_PIN = 6
        REVERSED = False

    class LeftRear:
        L_EN_PIN = None
        R_EN_PIN = None
        L_PWM_PIN = 5
        R_PWM_PIN = 4
        REVERSED = False

    class RightFront:
        L_EN_PIN = None
        R_EN_PIN = None
        L_PWM_PIN = 3
        R_PWM_PIN = 2
        REVERSED = True

    class RightRear:
        L_EN_PIN = None
        R_EN_PIN = None
        L_PWM_PIN = 1
        R_PWM_PIN = 0
        REVERSED = True

class ShooterConstants:
    class UpperFlywheel:
        PWM_PIN = 15
        REVERSED = True

    class LowerFlywheel:
        PWM_PIN = 14
        REVERSED = False

    class AngleAdj:
        CW_PIN = 8
        CLK_PIN = 9
        EN_PIN = 12
        REVERSED = True

class ConveyorConstants:
    class Spinner:
        PWM_PIN = 26
        REVERSED = False

    class Trigger:
        PWM_PIN = 28
        REVERSED = False
    
