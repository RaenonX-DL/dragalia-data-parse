"""Classes for handling the ability data."""
from dataclasses import dataclass, field
from typing import Optional, Union

from dlparse.enums import AbilityCondition, AbilityVariantType, SkillCondition, SkillNumber
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

    # K = min combo count; V = damage boost rate
    # - Highest combo first
    _combo_boost_data: list[tuple[int, float]] = field(default_factory=list)

    def __post_init__(self):
        if self.type_enum == AbilityVariantType.DMG_UP_ON_COMBO:
            # Variant type is boost on combo, parse the data
            for entry in self.id_str.split("/"):
                combo_count, boost_pct = entry.split("_")
                self._combo_boost_data.append((int(combo_count), float(boost_pct)))

    @property
    def is_not_used(self) -> bool:
        """Check if the variant is not used."""
        return self.type_enum == AbilityVariantType.NOT_USED

    @property
    def assigned_hit_label(self) -> Optional[str]:
        """Get the assigned hit label. Returns ``None`` if unavailable."""
        return self.id_str if self.type_enum == AbilityVariantType.CHANGE_STATE else None

    @property
    def assigned_action_condition(self) -> Optional[int]:
        """Get the assigned action condition ID. Returns ``None`` if unavailable."""
        return self.id_a if self.type_enum == AbilityVariantType.CHANGE_STATE else None

    @property
    def other_ability_id(self) -> Optional[int]:
        """Get the other ability ID assigned. Returns ``None`` if unavailable."""
        return self.id_a if self.type_enum == AbilityVariantType.OTHER_ABILITY else None

    @property
    def enhanced_skill(self) -> Optional[tuple[int, SkillNumber]]:
        """Get the enhanced skill ID and its skill number. Returns ``None`` if unavailable."""
        return (
            (self.id_a, SkillNumber.s1_s2_only(self.target_action_id - 2))
            if self.type_enum == AbilityVariantType.ENHANCE_SKILL else None
        )

    @property
    def is_boosted_by_combo(self) -> bool:
        """Check if the variant type is to boost the damage according to the combo count."""
        return self.type_enum == AbilityVariantType.DMG_UP_ON_COMBO

    def get_boost_by_combo(self, combo_count: int) -> float:
        """
        Get the total damage boost rate when the user combo count is ``combo_count``.

        The return will be 0.05 for 5% boost.
        """
        # Highest combo threshold first, reversing the data list
        for min_combo_count, dmg_up_pct in reversed(self._combo_boost_data):
            if combo_count >= min_combo_count:
                return dmg_up_pct / 100

        return 0


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
        return [variant.assigned_hit_label for variant in self.variants if variant.assigned_hit_label]

    @property
    def action_conditions(self) -> list[int]:
        """
        Get a list of hit labels assigned to the variants.

        Returns an empty list if no assigned label found.
        """
        return [variant.assigned_action_condition for variant in self.variants if variant.assigned_action_condition]

    @property
    def enhanced_skills(self) -> list[tuple[int, SkillNumber]]:
        """
        Get a list of skill IDs and numbers that will be enhanced if the ability condition holds.

        Returns an empty list if no skill enhancement found.
        """
        return [variant.enhanced_skill for variant in self.variants if variant.enhanced_skill]

    @property
    def variants(self) -> list[AbilityVariantEntry]:
        """
        Get all in-use ability variants as a list.

        Note that this does **not** give the other variants that come from different ability linked by the variants.
        To get all possible variants, call ``get_variants()`` instead.
        """
        return [variant for variant in (self.variant_1, self.variant_2, self.variant_3) if not variant.is_not_used]

    @property
    def is_boost_by_combo(self) -> bool:
        """Check if the damage will be boosted according to the current combo count."""
        return any(variant.is_boosted_by_combo for variant in self.variants)

    def get_variants(self, ability_asset: "AbilityAsset") -> list[AbilityVariantEntry]:
        """Get all variants bound to the ability."""
        variants_traverse: list[AbilityVariantEntry] = self.variants
        variants_return: list[AbilityVariantEntry] = []

        while variants_traverse:
            variant = variants_traverse.pop(0)
            other_ability_id = variant.other_ability_id

            if other_ability_id:
                variants_return.append(variant)
                variants_traverse.extend(ability_asset.get_data_by_id(other_ability_id).variants)

        return variants_return

    def get_all_ability(self, ability_asset: "AbilityAsset") -> dict[int, "AbilityEntry"]:
        """Get all the ability ID and the ability data possible from this ability, including self."""
        ret: dict[int, "AbilityEntry"] = {self.id: self}

        for variant in self.get_variants(ability_asset):
            other_ability_id = variant.other_ability_id

            if other_ability_id and other_ability_id not in ret:
                ret[other_ability_id] = ability_asset.get_data_by_id(other_ability_id)

        return ret

    def get_boost_by_combo(self, combo_count: int) -> float:
        """
        Get the total rate of damage boost when the user combo count is ``combo_count``.

        The return will be 0.05 for a total of 5% boost.
        """
        return sum(variant.get_boost_by_combo(combo_count) for variant in self.variants)

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "AbilityEntry":
        return AbilityEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            details_label=data["_Details"],
            condition=AbilityConditionEntry(
                data["_ConditionType"], data["_ConditionValue"], data["_ConditionValue2"]
            ),
            variant_1=AbilityVariantEntry(
                AbilityVariantType(data["_AbilityType1"]),
                data["_VariousId1a"], data["_VariousId1b"], data["_VariousId1c"],
                data["_VariousId1str"], data["_AbilityLimitedGroupId1"], data["_TargetAction1"],
                data["_AbilityType1UpValue"]
            ),
            variant_2=AbilityVariantEntry(
                AbilityVariantType(data["_AbilityType2"]),
                data["_VariousId2a"], data["_VariousId2b"], data["_VariousId2c"],
                data["_VariousId2str"], data["_AbilityLimitedGroupId2"], data["_TargetAction2"],
                data["_AbilityType2UpValue"]),
            variant_3=AbilityVariantEntry(
                AbilityVariantType(data["_AbilityType3"]),
                data["_VariousId3a"], data["_VariousId3b"], data["_VariousId3c"],
                data["_VariousId3str"], data["_AbilityLimitedGroupId3"], data["_TargetAction3"],
                data["_AbilityType3UpValue"]
            )
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
