from controllers.ibt_2 import IBT_2
from controllers.general_pwm import GeneralPWM
from controllers.spark_max import SparkMAX

__all__ = ["ControllerBase", "IBT_2", "GeneralPWM", "SparkMAX"]


class ControllerBase:
    def stop(self):
        raise NotImplementedError()
