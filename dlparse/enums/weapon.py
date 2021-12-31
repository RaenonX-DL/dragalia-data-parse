"""Enums for the weapons."""
from enum import Enum

from dlparse.errors import EnumConversionError, EnumNotFoundError
from .mixin import TranslatableEnumMixin

__all__ = ("Weapon",)


class Weapon(TranslatableEnumMixin, Enum):
    """Enums for the weapons."""

    UNKNOWN = -1

    NONE = 0

    SWD = 1  # Sword
    KAT = 2  # Blade (Katana)
    DAG = 3  # Dagger
    AXE = 4  # Axe
    LAN = 5  # Lance
    BOW = 6  # Bow
    ROD = 7  # Rod (Damaging Mage)
    CAN = 8  # Staff (Cane - Healing Mage)
    GUN = 9  # Manacaster (Gun)

    @property
    def is_valid(self) -> bool:
        """
        Check if the current weapon is valid.

        "Valid" means that this needs to be one of Sword, Blade, Dagger, Axe, Lance, Bow, Rod, Staff or Manacaster.
        """
        return self in self.get_all_valid_weapons()

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
        return [enum for enum in cls if enum not in (Weapon.NONE, Weapon.UNKNOWN)]

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

    @property
    def translation_id(self) -> str:
        return f"WEAPONTYPE_{self.name}"

    @staticmethod
    def get_all_translatable_members() -> list["Weapon"]:
        return Weapon.get_all_valid_weapons()

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN


_weapon_conv_dict: dict[Weapon, str] = {
    Weapon.SWD: "swd",
    Weapon.KAT: "kat",
    Weapon.DAG: "dag",
    Weapon.AXE: "axe",
    Weapon.LAN: "lan",
    Weapon.BOW: "bow",
    Weapon.ROD: "rod",
    Weapon.CAN: "can",
    Weapon.GUN: "gun",
}
