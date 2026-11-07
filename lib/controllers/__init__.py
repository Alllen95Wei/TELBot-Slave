class ControllerBase:
    def stop(self):
        raise NotImplementedError()

from controllers.ibt_2 import IBT_2
from controllers.general_pwm import GeneralPWM
from controllers.spark_max import SparkMAX
from controllers.tb6560 import TB6560

__all__ = ["ControllerBase", "IBT_2", "GeneralPWM", "SparkMAX", "TB6560"]
