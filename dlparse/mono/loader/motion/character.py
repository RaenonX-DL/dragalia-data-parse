"""Classes for loading the character motions."""
from dlparse.errors import MotionDataNotFoundError
from dlparse.mono.asset import CharaDataEntry, MotionControllerChara, MotionSelectorWeapon
from .base import MotionLoaderBase

__all__ = ("CharacterMotionLoader",)


class CharacterMotionLoader(MotionLoaderBase[MotionControllerChara, CharaDataEntry]):
    """Class to load the motion controller of a single character."""

    def __init__(self, motion_root_dir: str):
        super().__init__(motion_root_dir)
        self._motion_weapon: MotionSelectorWeapon = MotionSelectorWeapon(motion_root_dir)

    def get_motion_stop_time(self, chara_data: CharaDataEntry, motion_name: str) -> float:
        """Get the stop time of ``motion_name`` of a character."""
        ctrl_weapon = self._motion_weapon.get_controller(chara_data.weapon)

        try:
            ctrl_chara = self._get_motion_ctrl(chara_data, MotionControllerChara.load_from_file)
        except MotionDataNotFoundError:
            ctrl_chara = None

        return ctrl_weapon.get_stop_time_by_motion_name(motion_name, override=ctrl_chara, error_msg=chara_data.id)

    @staticmethod
    def get_controller_name(chara_data: CharaDataEntry) -> str:
        """Get the controller name of a character."""
        return f"{chara_data.weapon.weapon_str}_{chara_data.base_id}{chara_data.variation_id:02}"
