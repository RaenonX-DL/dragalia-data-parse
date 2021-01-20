"""Classes for handling the ability data."""
from dataclasses import dataclass, field
from typing import Optional, TextIO, Union

from dlparse.enums import AbilityCondition, AbilityVariantType, Condition, ConditionCategories, SkillNumber, Status
from dlparse.errors import AbilityConditionUnconvertibleError, AbilityOnSkillUnconvertibleError, EnumConversionError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("AbilityVariantEntry", "AbilityEntry", "AbilityAsset")

_ability_condition_map: dict[AbilityCondition, Condition] = {
    AbilityCondition.NONE: Condition.NONE,
    AbilityCondition.TRG_SELF_HP_LTE: Condition.ON_SELF_HP_LTE_30,
    AbilityCondition.TRG_RECEIVED_BUFF_DEF: Condition.ON_SELF_BUFFED_DEF,
    AbilityCondition.TRG_QUEST_START: Condition.QUEST_START,
    AbilityCondition.TRG_ENERGIZED: Condition.SELF_ENERGIZED,
    AbilityCondition.TRG_SHAPESHIFT_COMPLETED: Condition.SELF_SHAPESHIFT_COMPLETED,
}
"""
A dict that maps :class:`AbilityCondition` to :class:`Condition`.

This only contains :class:`AbilityCondition` that do not require additional parameter checks.
Missing key in this map does not mean that it is not handled.
"""

_hp_gte_map: dict[float, Condition] = {
    30: Condition.SELF_HP_GTE_30,
    40: Condition.SELF_HP_GTE_40,
    50: Condition.SELF_HP_GTE_50,
    60: Condition.SELF_HP_GTE_60,
    70: Condition.SELF_HP_GTE_70,
    85: Condition.SELF_HP_GTE_85,
    100: Condition.SELF_HP_FULL,
}
"""A dict that maps a certain HP threshold percentage to a :class:`Condition`."""


@dataclass
class AbilityConditionEntry:
    """Entry class for an ability condition."""

    condition_code: int

    val_1: float
    val_2: float

    cooldown_sec: float
    max_occurrences: int

    condition_type: AbilityCondition = field(init=False)

    def __post_init__(self):
        self.condition_type = AbilityCondition(self.condition_code)

    def _cond_self_buffed(self) -> Condition:
        if self.val_1 == 977 and self.val_2 == 978:
            # S!Mikoto, 977 for Illuminating Sunlight; 978 for Celestial Wavelight
            return Condition.SELF_SMIKOTO_CEL_SUN_WAVE

        if self.val_1 == 1380:
            return Condition.SELF_GLEONIDAS_FULL_STACKS

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    def _cond_self_hp(self) -> Optional[Condition]:
        # Self HP >=
        if self.condition_type in (AbilityCondition.EFF_SELF_HP_GTE, AbilityCondition.EFF_SELF_HP_GTE_2):
            return self._cond_self_hp_gte()

        # Self HP <
        if self.condition_type in (AbilityCondition.EFF_SELF_HP_LT, AbilityCondition.EFF_SELF_HP_LT_2):
            return self._cond_self_hp_lt()

        return None

    def _cond_self_hp_gte(self) -> Condition:
        if condition := _hp_gte_map.get(self.val_1):
            return condition

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    def _cond_self_hp_lt(self) -> Condition:
        if self.val_1 == 30:
            return Condition.SELF_HP_LT_30
        if self.val_1 == 40:
            return Condition.SELF_HP_LT_40

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    def _cond_self_in_dragon(self) -> Condition:
        if self.val_1 == 0 or self.val_1 == 1:
            return Condition.SELF_SHAPESHIFTED_1_TIME_IN_DRAGON
        if self.val_1 == 2:
            return Condition.SELF_SHAPESHIFTED_2_TIMES_IN_DRAGON

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    def _cond_hit_by_affliction(self) -> Condition:
        try:
            return ConditionCategories.trigger_hit_by_affliction.convert_reversed(Status(self.val_1))
        except EnumConversionError as ex:
            raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2) from ex

    def to_condition(self) -> Condition:
        """
        Convert the ability condition to condition.

        :raises AbilityConditionUnconvertibleError: if the ability condition is unconvertible
        """
        ability_condition = _ability_condition_map.get(self.condition_type)
        if ability_condition is not None:  # Explicit check because ``Condition.NONE`` is falsy
            return ability_condition

        # Self in-dragon
        if self.condition_type == AbilityCondition.EFF_IS_DRAGON:
            return self._cond_self_in_dragon()

        # Self HP condition
        if self_hp_cond := self._cond_self_hp():
            return self_hp_cond

        # Hit by attack with affliction
        if self.condition_type == AbilityCondition.TRG_HIT_WITH_AFFLICTION:
            return self._cond_hit_by_affliction()

        # Has specific buff
        if self.condition_type == AbilityCondition.EFF_SELF_SPECIFICALLY_BUFFED:
            return self._cond_self_buffed()

        raise AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

    @property
    def is_unknown_condition(self) -> bool:
        """Check if the condition type is unknown."""
        return self.condition_type == AbilityCondition.UNKNOWN


@dataclass
class AbilityVariantEntry:
    """A single ability variant class. This class is for a group of fields in :class:`AbilityEntry`."""

    type_id: int
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
    _def_boost_data: list[int] = field(default_factory=list)
    _skill_boost_data: list[int] = field(default_factory=list)

    type_enum: AbilityVariantType = field(init=False)

    def __post_init__(self):
        self.type_enum = AbilityVariantType(self.type_id)

        if self.type_enum == AbilityVariantType.DMG_UP_ON_COMBO:
            # Variant type is boost by combo
            for entry in self.id_str.split("/"):
                combo_count, boost_pct = entry.split("_")
                self._combo_boost_data.append((int(combo_count), float(boost_pct)))
        elif self.type_enum == AbilityVariantType.GAUGE_STATUS:
            # Variant type is boost by gauge status
            def_data, skill_boost_data = self.id_str.split("/", 1)

            self._def_boost_data = [0] + [int(boost_pct) for boost_pct in def_data.split("_")]
            self._skill_boost_data = [0] + [int(boost_pct) for boost_pct in skill_boost_data.split("_")]

    @property
    def is_not_used(self) -> bool:
        """Check if the variant is not used."""
        return self.type_enum == AbilityVariantType.NOT_USED

    @property
    def is_unknown_type(self):
        """Check if the variant type is unknown."""
        return self.type_enum == AbilityVariantType.UNKNOWN

    @property
    def is_boosted_by_combo(self) -> bool:
        """Check if the variant type is to boost the damage according to the combo count."""
        return self.type_enum == AbilityVariantType.DMG_UP_ON_COMBO

    @property
    def is_boosted_by_gauge_status(self) -> bool:
        """Check if the damage will be boosted according to the gauge status."""
        return self.type_enum == AbilityVariantType.GAUGE_STATUS

    @property
    def assigned_hit_label(self) -> Optional[str]:
        """Get the assigned hit label. Return ``None`` if unavailable."""
        return self.id_str if self.type_enum == AbilityVariantType.CHANGE_STATE else None

    @property
    def assigned_action_condition(self) -> Optional[int]:
        """Get the assigned action condition ID. Return ``None`` if unavailable."""
        return self.id_a if self.type_enum == AbilityVariantType.CHANGE_STATE else None

    @property
    def other_ability_id(self) -> Optional[int]:
        """Get the other ability ID assigned. Return ``None`` if unavailable."""
        return self.id_a if self.type_enum == AbilityVariantType.OTHER_ABILITY else None

    @property
    def enhanced_skill(self) -> Optional[tuple[int, SkillNumber]]:
        """Get the enhanced skill ID and its skill number. Return ``None`` if unavailable."""
        return (
            (self.id_a, SkillNumber.s1_s2_only(self.target_action_id - 2))
            if self.type_enum == AbilityVariantType.ENHANCE_SKILL else None
        )

    def get_boost_by_combo(self, combo_count: int) -> float:
        """
        Get the total damage boost rate when the user combo count is ``combo_count``.

        The return of 0.05 means 5% boost.
        """
        # Highest combo threshold first, reversing the data list
        for min_combo_count, dmg_up_pct in reversed(self._combo_boost_data):
            if combo_count >= min_combo_count:
                return dmg_up_pct / 100

        return 0

    def get_boost_by_gauge_filled_dmg(self, gauge_filled: int) -> float:
        """
        Get the total damage boost rate when ``gauge_filled`` gauges are filled.

        The return of 0.05 means 5% boost.
        """
        if not self._skill_boost_data:
            return 0

        return self._skill_boost_data[gauge_filled] / 100


@dataclass
class AbilityEntry(MasterEntryBase):
    """Single entry of an ability data."""

    name_label: str
    details_label: str

    condition: AbilityConditionEntry

    on_skill: int

    variant_1: AbilityVariantEntry
    variant_2: AbilityVariantEntry
    variant_3: AbilityVariantEntry

    @property
    def assigned_hit_labels(self) -> list[str]:
        """
        Get a list of hit labels assigned to the variants.

        Return an empty list if no assigned label found.
        """
        return [variant.assigned_hit_label for variant in self.variants if variant.assigned_hit_label]

    @property
    def action_conditions(self) -> list[int]:
        """
        Get a list of hit labels assigned to the variants.

        Return an empty list if no assigned label found.
        """
        return [variant.assigned_action_condition for variant in self.variants if variant.assigned_action_condition]

    @property
    def enhanced_skills(self) -> list[tuple[int, SkillNumber]]:
        """
        Get a list of skill IDs and numbers that will be enhanced if the ability condition holds.

        Return an empty list if no skill enhancement found.
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
    def unknown_variant_type_ids(self) -> list[int]:
        """Get a list of unknown variant type IDs."""
        return [variant.type_id for variant in self.variants if variant.is_unknown_type]

    @property
    def on_skill_condition(self) -> Condition:
        """
        Convert the on skill field to its corresponding condition.

        :raises AbilityOnSkillUnconvertibleError: unable to convert on skill condition to condition
        """
        # Value of `3` is a legacy one, usage unknown, currently no units are using it (2020/12/18)

        if self.on_skill == 0:
            return Condition.NONE

        if self.on_skill == 1:
            return Condition.SKILL_USED_S1

        if self.on_skill == 2:
            return Condition.SKILL_USED_S2

        if self.on_skill == 99:
            return Condition.SKILL_USED_ALL

        raise AbilityOnSkillUnconvertibleError(self.id, self.on_skill)

    @property
    def is_boost_by_combo(self) -> bool:
        """Check if the damage will be boosted according to the current combo count."""
        return any(variant.is_boosted_by_combo for variant in self.variants)

    @property
    def is_boost_by_gauge_status(self) -> bool:
        """Check if the damage will be boosted according to the gauge status."""
        return any(variant.is_boosted_by_gauge_status for variant in self.variants)

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
        Get the total damage boost rate when the user combo count is ``combo_count``.

        The return of 0.05 means a total pf 5% boost.
        """
        return sum(variant.get_boost_by_combo(combo_count) for variant in self.variants)

    def get_boost_by_gauge_filled_dmg(self, gauge_filled: int) -> float:
        """
        Get the total damage boost rate when ``gauge_filled`` gauges are filled.

        The return of 0.05 means a total pf 5% boost.
        """
        return sum(variant.get_boost_by_gauge_filled_dmg(gauge_filled) for variant in self.variants)

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "AbilityEntry":
        return AbilityEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            details_label=data["_Details"],
            condition=AbilityConditionEntry(
                data["_ConditionType"], data["_ConditionValue"], data["_ConditionValue2"],
                data["_CoolTime"], data["_OccurenceNum"]
            ),
            on_skill=data["_OnSkill"],
            variant_1=AbilityVariantEntry(
                data["_AbilityType1"],
                data["_VariousId1a"], data["_VariousId1b"], data["_VariousId1c"],
                data["_VariousId1str"], data["_AbilityLimitedGroupId1"], data["_TargetAction1"],
                data["_AbilityType1UpValue"]
            ),
            variant_2=AbilityVariantEntry(
                data["_AbilityType2"],
                data["_VariousId2a"], data["_VariousId2b"], data["_VariousId2c"],
                data["_VariousId2str"], data["_AbilityLimitedGroupId2"], data["_TargetAction2"],
                data["_AbilityType2UpValue"]
            ),
            variant_3=AbilityVariantEntry(
                data["_AbilityType3"],
                data["_VariousId3a"], data["_VariousId3b"], data["_VariousId3c"],
                data["_VariousId3str"], data["_AbilityLimitedGroupId3"], data["_TargetAction3"],
                data["_AbilityType3UpValue"]
            )
        )


class AbilityAsset(MasterAssetBase[AbilityEntry]):
    """Ability asset class."""

    asset_file_name = "AbilityData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(AbilityParser, file_location, asset_dir=asset_dir, file_like=file_like)


class AbilityParser(MasterParserBase[AbilityEntry]):
    """Class to parse the ability file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, AbilityEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: AbilityEntry.parse_raw(value) for key, value in entries.items()}
