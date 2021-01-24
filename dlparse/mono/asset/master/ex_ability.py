"""Classes for handling the EX ability asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Element, UnitType, Weapon
from dlparse.errors import AbilityConditionUnconvertibleError
from dlparse.mono.asset.base import (
    AbilityConditionEntryBase, AbilityEntryBase, AbilityVariantEntryBase, MasterAssetBase, MasterEntryBase,
    MasterParserBase,
)

__all__ = ("ExAbilityEntry", "ExAbilityAsset", "ExAbilityVariantEntry")


@dataclass
class ExAbilityConditionEntry(AbilityConditionEntryBase):
    """A single EX ability condition class. This class is for a group of fields in :class:`ExAbilityEntry`."""

    def _condition_unconvertible(self, ex: Optional[Exception] = None):
        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1)


@dataclass
class ExAbilityVariantEntry(AbilityVariantEntryBase):
    """A single EX ability variant class. This class is for a group of fields in :class:`ExAbilityEntry`."""


@dataclass
class ExAbilityEntry(AbilityEntryBase[ExAbilityConditionEntry, ExAbilityVariantEntry], MasterEntryBase):
    """Single entry of an EX ability data."""

    name_label: str
    details_label: str

    element: Element
    weapon: Weapon

    variant_1: ExAbilityVariantEntry
    variant_2: ExAbilityVariantEntry
    variant_3: ExAbilityVariantEntry

    @property
    def variants(self) -> list[ExAbilityVariantEntry]:
        return [variant for variant in (self.variant_1, self.variant_2, self.variant_3) if not variant.is_not_used]

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "ExAbilityEntry":
        return ExAbilityEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            details_label=data["_Details"],
            ability_icon_name=data["_AbilityIconName"],
            element=Element(data["_ElementalType"]),
            weapon=Weapon(data["_WeaponType"]),
            condition=ExAbilityConditionEntry(
                unit_type=UnitType(data["_UnitType"]), elemental_restriction=Element(data["_ElementalType"]),
                weapon_restriction=Weapon(data["_WeaponType"]),
                condition_code=data["_ConditionType"], val_1=data["_ConditionValue"], probability=data["_Probability"]
            ),
            variant_1=ExAbilityVariantEntry(
                type_id=data["_AbilityType1"], id_a=data["_VariousId1"], target_action_id=data["_TargetAction1"],
                up_value=data["_AbilityType1UpValue0"]
            ),
            variant_2=ExAbilityVariantEntry(
                type_id=data["_AbilityType2"], id_a=data["_VariousId2"], target_action_id=data["_TargetAction2"],
                up_value=data["_AbilityType2UpValue0"]
            ),
            variant_3=ExAbilityVariantEntry(
                type_id=data["_AbilityType3"], id_a=data["_VariousId3"], target_action_id=data["_TargetAction3"],
                up_value=data["_AbilityType3UpValue0"]
            ),
        )


class ExAbilityAsset(MasterAssetBase[ExAbilityEntry]):
    """Ex ability asset class."""

    asset_file_name = "ExAbilityData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(ExAbilityParser, file_location, asset_dir=asset_dir, file_like=file_like)


class ExAbilityParser(MasterParserBase[ExAbilityEntry]):
    """Class to parse the EX ability data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, ExAbilityEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: ExAbilityEntry.parse_raw(value) for key, value in entries.items()}
