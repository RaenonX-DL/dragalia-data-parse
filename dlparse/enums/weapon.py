"""Enums for the weapons."""
from enum import Enum

from dlparse.errors import EnumConversionError, EnumNotFoundError

__all__ = ("Weapon",)


class Weapon(Enum):
    """Enums for the weapons."""

    NONE = 0

    SWD = 1  # Sword
    KAT = 2  # Katana
    DAG = 3  # Dagger
    AXE = 4  # Axe
    LAN = 5  # Lance
    BOW = 6  # Bow
    ROD = 7  # Rod (Damaging Mage)
    CAN = 8  # Cane (Healing Mage)
    GUN = 9  # Gun

    @property
    def weapon_str(self) -> str:
        """
        Get the weapon string.

        :raises EnumNotFoundError: if the current weapon does not correspond to any weapon string
        """
        if self not in _weapon_conv_dict:
            raise EnumConversionError(self, Weapon, "weapon string")

        return _weapon_conv_dict[self]

    @classmethod
    def get_all_valid_weapons(cls) -> list["Weapon"]:
        """
        Get all valid weapons.

        This will **not** return ``Weapon.NONE`` as it serves as a sentinel value in the data only.
        """
        return [enum for enum in cls if enum != Weapon.NONE]

    @staticmethod
    def from_str(weapon_str: str) -> "Weapon":
        """
        Convert ``weapon_str`` to its corresponding :class:`Weapon`.

        Note that the comparison is case-insensitive.

        :raises EnumNotFoundError: if `weapon_str` does not correspond to any `Weapon`
        """
        weapon_str = weapon_str.lower()

        for weapon, code in _weapon_conv_dict.items():
            if code == weapon_str:
                return weapon

        raise EnumNotFoundError(Weapon, weapon_str)


_weapon_conv_dict: dict[Weapon, str] = {
    Weapon.SWD: "swd",
    Weapon.KAT: "kat",
    Weapon.DAG: "dag",
    Weapon.AXE: "axe",
    Weapon.LAN: "lan",
    Weapon.BOW: "bow",
    Weapon.ROD: "rod",
    Weapon.CAN: "can",
    Weapon.GUN: "gun"
}
