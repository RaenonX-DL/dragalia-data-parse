"""Classes for handling the ability data."""
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, TextIO, Union

from dlparse.enums import AbilityCondition, AbilityVariantType, Condition, Element, SkillNumber, UnitType, Weapon
from dlparse.errors import AbilityConditionUnconvertibleError, AbilityOnSkillUnconvertibleError
from dlparse.mono.asset.base import (
    AbilityConditionEntryBase, AbilityVariantEntryBase, MasterAssetBase, MasterEntryBase,
    MasterParserBase,
)
from dlparse.mono.asset.extension import AbilityEntryExtension

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityVariantEntry", "AbilityEntry", "AbilityAsset")


@dataclass
class AbilityConditionEntry(AbilityConditionEntryBase):
    """Entry class for an ability condition."""

    val_2: float

    cooldown_sec: float
    max_occurrences: int

    def __post_init__(self):
        super().__post_init__()

        self.condition_type = AbilityCondition(self.condition_code)

    def _condition_unconvertible(self, ex: Optional[Exception] = None):
        error = AbilityConditionUnconvertibleError(self.condition_code, self.val_1, self.val_2)

        if ex:
            raise error from ex

        raise error

    def _cond_self_buffed_additional(self) -> Optional[Condition]:
        if self.val_1 == 977 and self.val_2 == 978:
            # S!Mikoto, 977 for Illuminating Sunlight; 978 for Celestial Wavelight
            return Condition.SELF_SMIKOTO_CEL_SUN_WAVE

        return None

    @property
    def max_stack_count(self) -> int:
        if self.condition_type == AbilityCondition.TRG_COMBO_COUNT_DIV_LIMITED:
            return int(self.val_2)

        return super().max_stack_count


@dataclass
class AbilityVariantEntry(AbilityVariantEntryBase):
    """A single ability variant class. This class is for a group of fields in :class:`AbilityEntry`."""

    id_b: int
    id_c: int
    id_str: str
    limited_group_id: int

    # K = min combo count; V = damage boost rate
    # - Highest combo first
    _combo_boost_data: list[tuple[int, float]] = field(default_factory=list)
    _def_boost_data: list[int] = field(default_factory=list)
    _skill_boost_data: list[int] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()

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
    def assigned_hit_label(self) -> Optional[str]:
        """Get the assigned hit label. Return ``None`` if unavailable."""
        return self.id_str if self.type_enum == AbilityVariantType.CHANGE_STATE else None

    def get_action_cond_id_hit_label(self, asset_manager: "AssetManager") -> Optional[int]:
        """Get the action condition ID of the hit label, if assigned. Return ``None`` if inapplicable."""
        # Check if the hit label is assigned & available
        if not (hit_label := self.assigned_hit_label):
            return None

        # Check if the hit attribute data is available
        if not (hit_attr := asset_manager.asset_hit_attr.get_data_by_id(hit_label)):
            return None

        # Check if the hit attribute has action condition assigned
        if not hit_attr.has_action_condition:
            return None

        return hit_attr.action_condition_id

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
class AbilityEntry(AbilityEntryExtension[AbilityConditionEntry, AbilityVariantEntry], MasterEntryBase):
    """Single entry of an ability data."""

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
        return [variant for variant in (self.variant_1, self.variant_2, self.variant_3) if not variant.is_not_used]

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
        """Get all variants bound to the ability, including the ones that branched from a certain ability."""
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
            description_label=data["_Details"],
            ability_icon_name=data["_AbilityIconName"],
            condition=AbilityConditionEntry(
                unit_type=UnitType(data["_UnitType"]), elemental_restriction=Element(data["_ElementalType"]),
                weapon_restriction=Weapon(data["_WeaponType"]),
                condition_code=data["_ConditionType"], val_1=data["_ConditionValue"], val_2=data["_ConditionValue2"],
                probability=data["_Probability"], cooldown_sec=data["_CoolTime"], max_occurrences=data["_OccurenceNum"]
            ),
            on_skill=data["_OnSkill"],
            variant_1=AbilityVariantEntry(
                type_id=data["_AbilityType1"],
                id_a=data["_VariousId1a"], id_b=data["_VariousId1b"], id_c=data["_VariousId1c"],
                id_str=data["_VariousId1str"], limited_group_id=data["_AbilityLimitedGroupId1"],
                target_action_id=data["_TargetAction1"], up_value=data["_AbilityType1UpValue"]
            ),
            variant_2=AbilityVariantEntry(
                type_id=data["_AbilityType2"],
                id_a=data["_VariousId2a"], id_b=data["_VariousId2b"], id_c=data["_VariousId2c"],
                id_str=data["_VariousId2str"], limited_group_id=data["_AbilityLimitedGroupId2"],
                target_action_id=data["_TargetAction2"], up_value=data["_AbilityType2UpValue"]
            ),
            variant_3=AbilityVariantEntry(
                type_id=data["_AbilityType3"],
                id_a=data["_VariousId3a"], id_b=data["_VariousId3b"], id_c=data["_VariousId3c"],
                id_str=data["_VariousId3str"], limited_group_id=data["_AbilityLimitedGroupId3"],
                target_action_id=data["_TargetAction3"], up_value=data["_AbilityType3UpValue"]
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
