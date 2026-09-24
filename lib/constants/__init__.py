__all__ = ["GeneralConstants", "ChassisConstants"]

class GeneralConstants:
    class UART:
        BAUD_RATE = 115200
        TX_PIN = 0
        RX_PIN = 1

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
