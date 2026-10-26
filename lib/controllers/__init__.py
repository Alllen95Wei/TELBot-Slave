from controllers.ibt_2 import IBT_2

__all__ = ["ControllerBase", "IBT_2"]


class ControllerBase:
    def stop(self):
        raise NotImplementedError()
