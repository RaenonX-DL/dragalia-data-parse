"""Classes for loading the character motions."""
from dlparse.errors import MotionDataNotFoundError
from dlparse.mono.asset import CharaDataEntry, MotionControllerChara, MotionSelectorWeapon

__all__ = ("CharacterMotionLoader",)


class CharacterMotionLoader:
    """Class to load the motion controller of a single character."""

    def __init__(self, motion_root_dir: str):
        self._motion_root: str = motion_root_dir
        self._motion_weapon: MotionSelectorWeapon = MotionSelectorWeapon(motion_root_dir)

        self._motion_cache: dict[str, MotionControllerChara] = {}

    def _get_character_motion(self, chara_data: CharaDataEntry) -> MotionControllerChara:
        name = self.get_controller_name(chara_data)

        if name not in self._motion_cache:
            self._motion_cache[name] = MotionControllerChara.load_from_file(self._motion_root, f"{name}.json")

        return self._motion_cache[name]

    def get_character_motion_stop_time(self, chara_data: CharaDataEntry, motion_name: str) -> float:
        """Get the stop time of ``motion_name`` of a character."""
        name = self.get_controller_name(chara_data)

        ctrl_motion = self._motion_weapon.get_controller(chara_data.weapon)
        try:
            ctrl_chara = self._get_character_motion(chara_data)
        except FileNotFoundError as ex:
            raise MotionDataNotFoundError(name) from ex

        try:
            original_clip_id = ctrl_motion.get_clip_id_by_motion_name(motion_name)
        except KeyError as ex:
            raise MotionDataNotFoundError(motion_name, chara_data.id) from ex

        if ctrl_chara.is_clip_overridden(original_clip_id):
            return ctrl_chara.get_stop_time_by_original_clip_id(original_clip_id)

        return ctrl_motion.get_stop_time_by_clip_id(original_clip_id)

    @staticmethod
    def get_controller_name(chara_data: CharaDataEntry) -> str:
        """Get the controller name of a character."""
        return f"{chara_data.weapon.weapon_str}_{chara_data.base_id}{chara_data.variation_id:02}"
