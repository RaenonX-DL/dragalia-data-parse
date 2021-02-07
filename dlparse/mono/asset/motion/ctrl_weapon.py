"""Motion controller classes for a single weapon type."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.enums import Weapon
from dlparse.mono.asset.extension import AnimatorController
from .selector import MotionSelectorBase

__all__ = ("MotionControllerWeapon", "MotionSelectorWeapon")


@dataclass
class MotionControllerWeapon(AnimatorController):
    """Motion controller for a single weapon type."""

    weapon: Weapon = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        controller = self.json_dict["$Controller"]
        self.weapon = Weapon.from_str(controller["m_Name"])

    @staticmethod
    def parse_raw(data: dict[str, Any]) -> "MotionControllerWeapon":
        return MotionControllerWeapon(data)


@dataclass
class MotionSelectorWeapon(MotionSelectorBase[Weapon, MotionControllerWeapon]):
    """Class to select the controller to be used based on the weapon type."""

    def __init__(self, motion_dir: str):
        motion_map = {weapon: f"{weapon.weapon_str}.json" for weapon in Weapon.get_all_valid_weapons()}

        super().__init__(MotionControllerWeapon, motion_dir, motion_map)
