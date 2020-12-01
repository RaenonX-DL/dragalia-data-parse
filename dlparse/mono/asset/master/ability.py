"""Classes for handling the ability data."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.enums import AbilityCondition, AbilityType, SkillCondition
from dlparse.errors import AbilityConditionUnconvertibleError
from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("AbilityEntry", "AbilityAsset", "AbilityParser")


@dataclass
class AbilityConditionEntry:
    """Entry class for an ability condition."""

    condition_type: AbilityCondition
    val_1: float
    val_2: float

    def to_skill_condition(self) -> SkillCondition:
        """
        Convert the ability condition to skill condition.

        :raises AbilityConditionUnconvertibleError: if the ability condition is unconvertible
        """
        if self.condition_type == AbilityCondition.NONE:
            return SkillCondition.NONE

        if self.condition_type == AbilityCondition.SELF_HP_GTE:
            if self.val_1 == 40:
                return SkillCondition.SELF_HP_GTE_40
            if self.val_1 == 50:
                return SkillCondition.SELF_HP_GTE_50

        if self.condition_type == AbilityCondition.SELF_HP_LT:
            if self.val_1 == 40:
                return SkillCondition.SELF_HP_LT_40

        raise AbilityConditionUnconvertibleError(self.condition_type, self.val_1, self.val_2)


@dataclass
class AbilityVariantEntry:
    """A single ability variant class. This class is for a group of fields in :class:`AbilityEntry`."""

    type_enum: AbilityType
    id_a: int
    id_b: int
    id_c: int
    id_str: str
    limited_group_id: int
    target_action_id: int
    up_value: float

    @property
    def assigned_hit_label(self) -> Optional[str]:
        """Get the assigned hit label, if the type matches. If the type does not match, returns ``None`` instead."""
        return self.id_str if self.type_enum == AbilityType.TO_HIT_ATTR_ON_MATCH else None

    @property
    def other_ability_id(self) -> Optional[int]:
        """
        Get the other ability ID assigned.

        If the type does not match, returns ``None`` instead.
        """
        return self.id_a if self.type_enum == AbilityType.TO_ABILITY_OTHER else None


@dataclass
class AbilityEntry(MasterEntryBase):
    """Single entry of an ability data."""

    name_label: str
    details_label: str

    condition: AbilityConditionEntry

    variant_1: AbilityVariantEntry
    variant_2: AbilityVariantEntry
    variant_3: AbilityVariantEntry

    @property
    def assigned_hit_labels(self) -> list[str]:
        """
        Get a list of hit labels assigned to the variants.

        Returns an empty list if no assigned label found.
        """
        return [variant.assigned_hit_label for variant in (self.variant_1, self.variant_2, self.variant_3)
                if variant.assigned_hit_label]

    @property
    def get_other_ability_ids(self) -> list[int]:
        """Get a list of ability ID variants on ability condition mismatched."""
        return [variant.other_ability_id for variant in (self.variant_1, self.variant_2, self.variant_3)
                if variant.other_ability_id]

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "AbilityEntry":
        return AbilityEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            details_label=data["_Details"],
            condition=AbilityConditionEntry(AbilityCondition(data["_ConditionType"]),
                                            data["_ConditionValue"], data["_ConditionValue2"]),
            variant_1=AbilityVariantEntry(AbilityType(data["_AbilityType1"]),
                                          data["_VariousId1a"], data["_VariousId1b"], data["_VariousId1c"],
                                          data["_VariousId1str"], data["_AbilityLimitedGroupId1"],
                                          data["_TargetAction1"], data["_AbilityType1UpValue"]),
            variant_2=AbilityVariantEntry(AbilityType(data["_AbilityType2"]),
                                          data["_VariousId2a"], data["_VariousId2b"], data["_VariousId2c"],
                                          data["_VariousId2str"], data["_AbilityLimitedGroupId2"],
                                          data["_TargetAction2"], data["_AbilityType2UpValue"]),
            variant_3=AbilityVariantEntry(AbilityType(data["_AbilityType3"]),
                                          data["_VariousId3a"], data["_VariousId3b"], data["_VariousId3c"],
                                          data["_VariousId3str"], data["_AbilityLimitedGroupId3"],
                                          data["_TargetAction3"], data["_AbilityType3UpValue"])
        )


class AbilityAsset(MasterAssetBase[AbilityEntry]):
    """Ability asset class."""

    asset_file_name = "AbilityData.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(AbilityParser, file_path, asset_dir=asset_dir)


class AbilityParser(MasterParserBase[AbilityEntry]):
    """Class to parse the ability file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, AbilityEntry]:
        entries = cls.get_entries(file_path)

        return {key: AbilityEntry.parse_raw(value) for key, value in entries.items()}
