"""Classes for handling the ability data."""
from dataclasses import dataclass, field
from typing import Optional, Union

from dlparse.enums import AbilityCondition, AbilityVariantType, SkillCondition
from dlparse.errors import AbilityConditionUnconvertibleError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("AbilityEntry", "AbilityAsset", "AbilityParser")


@dataclass
class AbilityConditionEntry:
    """Entry class for an ability condition."""

    condition_code: int

    val_1: float
    val_2: float

    condition_type: AbilityCondition = field(init=False)

    def __post_init__(self):
        self.condition_type = AbilityCondition(self.condition_code)

    def _skill_cond_self_hp_gt(self):
        if self.val_1 == 30:
            return SkillCondition.SELF_HP_GT_30

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    def _skill_cond_self_hp_gte(self):
        if self.val_1 == 40:
            return SkillCondition.SELF_HP_GTE_40
        if self.val_1 == 50:
            return SkillCondition.SELF_HP_GTE_50
        if self.val_1 == 60:
            return SkillCondition.SELF_HP_GTE_60
        if self.val_1 == 85:
            return SkillCondition.SELF_HP_GTE_85

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    def _skill_cond_self_hp_lt(self):
        if self.val_1 == 30:
            return SkillCondition.SELF_HP_LT_30
        if self.val_1 == 40:
            return SkillCondition.SELF_HP_LT_40

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    def to_skill_condition(self) -> SkillCondition:
        """
        Convert the ability condition to skill condition.

        :raises AbilityConditionUnconvertibleError: if the ability condition is unconvertible
        """
        # No condition
        if self.condition_type == AbilityCondition.NONE:
            return SkillCondition.NONE

        # Self HP >
        if self.condition_type == AbilityCondition.SELF_HP_GT:
            return self._skill_cond_self_hp_gt()

        # Self HP >=
        if self.condition_type == AbilityCondition.SELF_HP_GTE:
            return self._skill_cond_self_hp_gte()

        # Self HP <
        if self.condition_type in (AbilityCondition.SELF_HP_LT, AbilityCondition.SELF_HP_LT_2):
            return self._skill_cond_self_hp_lt()

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)


@dataclass
class AbilityVariantEntry:
    """A single ability variant class. This class is for a group of fields in :class:`AbilityEntry`."""

    type_enum: AbilityVariantType
    id_a: int
    id_b: int
    id_c: int
    id_str: str
    limited_group_id: int
    target_action_id: int
    up_value: float

    @property
    def assigned_hit_label(self) -> Optional[str]:
        """Get the assigned hit label, if the type matches. Returns ``None`` if unavailable."""
        return self.id_str if self.type_enum == AbilityVariantType.CHANGE_STATE else None

    @property
    def other_ability_id(self) -> Optional[int]:
        """Get the other ability ID assigned. Returns ``None`` if unavailable."""
        return self.id_a if self.type_enum == AbilityVariantType.OTHER_ABILITY else None

    @property
    def enhanced_skill(self) -> Optional[tuple[int, int]]:
        """Get the enhanced skill ID and its skill number. Returns ``None`` if unavailable."""
        return (self.id_a, self.target_action_id - 2) if self.type_enum == AbilityVariantType.ENHANCE_SKILL else None


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
    def variants(self) -> list[AbilityVariantEntry]:
        """Get all ability variants as a list."""
        return [self.variant_1, self.variant_2, self.variant_3]

    @property
    def assigned_hit_labels(self) -> list[str]:
        """
        Get a list of hit labels assigned to the variants.

        Returns an empty list if no assigned label found.
        """
        return [variant.assigned_hit_label for variant in self.variants if variant.assigned_hit_label]

    @property
    def other_ability_ids(self) -> list[int]:
        """
        Get a list of ability IDs that are being referenced by the variants.

        Returns an empty list if no other ability IDs available.
        """
        return [variant.other_ability_id for variant in self.variants if variant.other_ability_id]

    @property
    def enhanced_skills(self) -> list[tuple[int, int]]:
        """
        Get a list of skills that may be enhanced if the ability condition holds.

        The 1st element is the skill ID; the 2nd element is the skill number.

        Returns an empty list if no enhanced skill variants available.
        """
        return [variant.enhanced_skill for variant in self.variants if variant.enhanced_skill]

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "AbilityEntry":
        return AbilityEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            details_label=data["_Details"],
            condition=AbilityConditionEntry(data["_ConditionType"],
                                            data["_ConditionValue"], data["_ConditionValue2"]),
            variant_1=AbilityVariantEntry(AbilityVariantType(data["_AbilityType1"]),
                                          data["_VariousId1a"], data["_VariousId1b"], data["_VariousId1c"],
                                          data["_VariousId1str"], data["_AbilityLimitedGroupId1"],
                                          data["_TargetAction1"], data["_AbilityType1UpValue"]),
            variant_2=AbilityVariantEntry(AbilityVariantType(data["_AbilityType2"]),
                                          data["_VariousId2a"], data["_VariousId2b"], data["_VariousId2c"],
                                          data["_VariousId2str"], data["_AbilityLimitedGroupId2"],
                                          data["_TargetAction2"], data["_AbilityType2UpValue"]),
            variant_3=AbilityVariantEntry(AbilityVariantType(data["_AbilityType3"]),
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
