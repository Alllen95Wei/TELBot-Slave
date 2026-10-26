from subsystems.chassis import Chassis
from subsystems.shooter import Shooter

from controllers import ControllerBase

__all__ = ["SubsystemBase", "Chassis", "Shooter"]


class SubsystemBase:
    motors: set[ControllerBase]

    def stop_all(self):
        """Stop all motors/devices in this subsystem."""
        for motor in self.motors:
            motor.stop()
