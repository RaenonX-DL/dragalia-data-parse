"""Classes for loading the dragon motions."""
from dlparse.mono.asset import DragonDataEntry, MotionControllerDragon
from .base import MotionLoaderBase

__all__ = ("DragonMotionLoader",)


class DragonMotionLoader(MotionLoaderBase[MotionControllerDragon, DragonDataEntry]):
    """Class to load the motion controller of a single dragon."""

    def get_motion_stop_time(self, entry: DragonDataEntry, motion_name: str) -> float:
        """
        Get the stop time of ``motion_name`` of a dragon.

        :raises MotionDataNotFoundError: if the motion data of ``dragon_data`` is not found
        """
        ctrl_dragon = self._get_motion_ctrl(entry, MotionControllerDragon.load_from_file)

        return ctrl_dragon.get_stop_time_by_motion_name(motion_name)

    @staticmethod
    def get_controller_name(entry: DragonDataEntry) -> str:
        """Get the controller name of a dragon."""
        return f"d{entry.base_id}_{entry.variation_id:02}"
