"""Classes for handling the action condition asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Condition, ConditionCategories, EfficacyType, Element, ElementFlag, Status
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("ActionConditionEntry", "ActionConditionAsset")


@dataclass
class ActionConditionEntry(MasterEntryBase):
    """Single entry of an action condition data."""

    afflict_status: Status

    overwrite_group_id: int
    overwrite_identical_owner: int

    max_instance_count: int

    duration_sec: float
    duration_count: float
    duration_count_max: int
    """
    Maximum count of the buffs stackable.

    ``0`` means not applicable (``duration_count`` = 0, most likely is a buff limited by time duration).

    ``1`` means unstackable.

    Any positive number means the maximum count of stacks possible.
    """

    probability_pct: float

    efficacy_type: EfficacyType

    slip_interval_sec: float
    slip_damage_mod: float
    slip_damage_hp_rate: float

    regen_rp: float
    regen_sp_pct: float

    buff_atk: float
    buff_def: float
    buff_def_b: float
    buff_crt_rate: float
    buff_crt_damage: float
    buff_skill_damage: float
    buff_fs_damage: float
    buff_atk_spd: float
    buff_fs_spd: float
    buff_sp_rate: float

    shield_dmg: float
    shield_hp: float

    damage_reduction: float

    resistance_flame: float
    resistance_water: float
    resistance_wind: float
    resistance_light: float
    resistance_shadow: float

    resistance_poison: float
    resistance_burn: float
    resistance_freeze: float
    resistance_paralyze: float
    resistance_blind: float
    resistance_stun: float
    resistance_curse: float
    resistance_bog: float
    resistance_sleep: float
    resistance_frostbite: float
    resistance_flashburn: float
    resistance_stormlash: float
    resistance_shadowblight: float
    resistance_scorchrend: float

    enhance_fs_action_id: int
    enhance_skill_1_id: int
    enhance_skill_2_id: int

    energize_lv: int
    inspire_lv: int

    hp_drain_rate: float

    elemental_target: ElementFlag

    level_up_id: int
    level_down_id: int

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "ActionConditionEntry":
        duration_count_max = (
            data["_MaxDurationNum"] if data["_IsAddDurationNum"] else 1
            if data["_DurationNum"]
            else 0
        )
        regen_sp_pct = (
            -data["_SlipDamageRatio"] * 100 / data["_SlipDamageIntervalSec"]
            if data["_UniqueRegeneSp01"] or data["_AutoRegeneS1"]
            else 0
        )

        return ActionConditionEntry(
            id=data["_Id"],
            afflict_status=Status(data["_Type"]),
            overwrite_group_id=data["_OverwriteGroupId"],
            overwrite_identical_owner=data["_OverwriteIdenticalOwner"],
            max_instance_count=data["_MaxDuplicatedCount"],
            duration_sec=data["_DurationSec"],
            duration_count=data["_DurationNum"],
            duration_count_max=duration_count_max,
            probability_pct=data["_Rate"],
            efficacy_type=EfficacyType(data["_EfficacyType"]),
            slip_interval_sec=data["_SlipDamageIntervalSec"],
            slip_damage_mod=data["_SlipDamagePower"],
            slip_damage_hp_rate=data["_SlipDamageRatio"],
            regen_rp=data["_RegenePower"],
            regen_sp_pct=regen_sp_pct,
            buff_atk=data["_RateAttack"],
            buff_def=data["_RateDefense"],
            buff_def_b=data["_RateDefenseB"],
            buff_crt_rate=data["_RateCritical"],
            buff_crt_damage=data["_EnhancedCritical"],
            buff_skill_damage=data["_RateSkill"],
            buff_fs_damage=data["_RateBurst"],
            buff_atk_spd=data["_RateAttackSpeed"],
            buff_sp_rate=data["_RateRecoverySp"],
            buff_fs_spd=data["_RateChargeSpeed"],
            shield_dmg=data["_RateDamageShield"],
            shield_hp=data["_RateSacrificeShield"],
            damage_reduction=data["_RateDamageCut"],
            resistance_flame=data["_RateFire"],
            resistance_water=data["_RateWater"],
            resistance_wind=data["_RateWind"],
            resistance_light=data["_RateLight"],
            resistance_shadow=data["_RateDark"],
            resistance_poison=data["_RatePoison"],
            resistance_burn=data["_RateBurn"],
            resistance_freeze=data["_RateFreeze"],
            resistance_paralyze=data["_RateParalysis"],
            resistance_blind=data["_RateDarkness"],
            resistance_stun=data["_RateSwoon"],
            resistance_curse=data["_RateCurse"],
            resistance_bog=data["_RateSlowMove"],
            resistance_sleep=data["_RateSleep"],
            resistance_frostbite=data["_RateFrostbite"],
            resistance_flashburn=data["_RateFlashheat"],
            resistance_stormlash=data["_RateCrashWind"],
            resistance_shadowblight=data["_RateDarkAbs"],
            resistance_scorchrend=data["_RateDestroyFire"],
            enhance_fs_action_id=data["_EnhancedBurstAttack"],
            enhance_skill_1_id=data["_EnhancedSkill1"],
            enhance_skill_2_id=data["_EnhancedSkill2"],
            energize_lv=data["_Tension"],
            inspire_lv=data["_Inspiration"],
            hp_drain_rate=data["_RateHpDrain"],
            elemental_target=ElementFlag(data["_TargetElemental"]),
            level_up_id=data["_LevelUpId"],
            level_down_id=data["_LevelDownId"]
        )

    @property
    def conditions(self) -> list[Condition]:
        """
        Get the conditions for this action condition to be effective.

        If no conditions are required, return an empty list.

        If any of the conditions returned matches, then the action condition is considered effective.
        """
        if not self.target_limited_by_element:
            # Not limited to certain element, no condition
            return []

        return [
            ConditionCategories.target_element.convert_reversed(element)
            for element in Element.from_flag(self.elemental_target)
        ]

    @property
    def target_limited_by_element(self):
        """Check if the action condition will be limited by the element of the target."""
        return self.elemental_target.is_effective

    @property
    def max_stack_count(self) -> int:
        """Get the maximum stack count of action condition. ``0`` means not applicable."""
        return (self.duration_count_max
                or int(bool(self.overwrite_group_id))
                or int(bool(self.overwrite_identical_owner)))

    @property
    def is_dispel_buff(self) -> bool:
        """Check if the action condition dispelling the buff."""
        return self.efficacy_type == EfficacyType.DISPEL

    @property
    def is_leveled(self) -> bool:
        """Check if the action condition is leveled."""
        return bool(self.level_up_id or self.level_down_id)


class ActionConditionAsset(MasterAssetBase[ActionConditionEntry]):
    """Action condition asset class."""

    asset_file_name = "ActionCondition.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(ActionConditionParser, file_location, asset_dir=asset_dir, file_like=file_like)


class ActionConditionParser(MasterParserBase[ActionConditionEntry]):
    """Class to parse the action condition file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, ActionConditionEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: ActionConditionEntry.parse_raw(value) for key, value in entries.items()}
