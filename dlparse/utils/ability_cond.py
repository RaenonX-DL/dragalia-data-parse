"""Classes for handling ability condition."""
from typing import Optional, TypeVar

from dlparse.enums import BuffParameter, HitTargetSimple, SkillIndex, Status
from dlparse.errors import UnhandledSelfDamageError
from dlparse.model import ActionConditionEffectUnit, AfflictionEffectUnit, HitData
from dlparse.mono.asset import ActionConditionAsset, ActionConditionEntry, HitAttrEntry

__all__ = ("AbilityConditionConverter",)

HT = TypeVar("HT", bound=HitData)


class AbilityConditionConverter:
    """Class for converting an ability condition entry to units of effects."""

    @staticmethod
    def to_param_up(
            param_enum: BuffParameter, param_rate: float,
            hit_data: HT, cond_entry: Optional[ActionConditionEntry]
    ) -> Optional[ActionConditionEffectUnit]:
        """
        Creates an effect unit (if applicable) based on the given data.

        If ``param_rate`` is ``0`` (meaning not used), ``None`` will be returned instead.

        if ``cond_entry`` is ``None``, both ``duration_time`` and ``duration_count`` will set to 0.
        """
        if not param_rate:  # Param rate = 0 means not applicable
            return None

        return ActionConditionEffectUnit(
            time=hit_data.action_time,
            status=Status.NONE,
            target=hit_data.target_simple,
            parameter=param_enum,
            probability_pct=cond_entry.probability_pct if cond_entry else 0,
            rate=param_rate,
            slip_interval=cond_entry.slip_interval if cond_entry else 0,
            slip_damage_mod=cond_entry.slip_damage_mod if cond_entry else 0,
            duration_time=hit_data.get_duration(cond_entry),
            duration_count=cond_entry.duration_count if cond_entry else 0,
            hit_attr_label=hit_data.hit_attr.id,
            action_cond_id=hit_data.hit_attr.action_condition_id,
            max_stack_count=cond_entry.max_stack_count if cond_entry else 0
        )

    @staticmethod
    def to_damage_self(starting_time: float, hit_attr: HitAttrEntry) -> Optional[ActionConditionEffectUnit]:
        """
        Returns the corresponding :class:`ActionConditionEffectUnit` if the hit attribute will self damage.

        Returns ``None`` if not self damaging.

        :raises UnhandledSelfDamageError: if the self damage ability is unhandled
        """
        if not hit_attr.is_damage_self:
            return None

        if hit_attr.hp_fix_rate:
            return ActionConditionEffectUnit(
                time=starting_time,
                status=Status.NONE,
                probability_pct=100,
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.HP_FIX_BY_MAX,
                rate=hit_attr.hp_fix_rate,
                slip_interval=0,
                slip_damage_mod=0,
                duration_time=0,
                duration_count=0,
                hit_attr_label=hit_attr.id,
                action_cond_id=hit_attr.action_condition_id,
                max_stack_count=0
            )

        if hit_attr.hp_consumption_rate:
            return ActionConditionEffectUnit(
                time=starting_time,
                status=Status.NONE,
                probability_pct=100,
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.HP_DECREASE_BY_MAX,
                rate=hit_attr.hp_consumption_rate,
                slip_interval=0,
                slip_damage_mod=0,
                duration_time=0,
                duration_count=0,
                hit_attr_label=hit_attr.id,
                action_cond_id=hit_attr.action_condition_id,
                max_stack_count=0
            )

        raise UnhandledSelfDamageError(hit_attr.id)

    @staticmethod
    def to_affliction_unit(
            hit_data: HT, asset_action_condition: ActionConditionAsset
    ) -> Optional[AfflictionEffectUnit]:
        """Get the affliction effect unit of ``hit_data``. Returns ``None`` if not applicable."""
        if not hit_data.hit_attr.action_condition_id:
            # No action condition affiliated
            return None

        if not hit_data.target_simple == HitTargetSimple.ENEMY:
            # Target not enemy
            return None

        action_cond_data = asset_action_condition.get_data_by_id(hit_data.hit_attr.action_condition_id)

        if not action_cond_data.afflict_status.is_abnormal_status:
            # Not afflicting action condition
            return None

        return AfflictionEffectUnit(
            time=hit_data.action_component.time_start,
            status=action_cond_data.afflict_status,
            target=hit_data.target_simple,
            probability_pct=action_cond_data.probability_pct,
            parameter=BuffParameter.AFFLICTION,
            duration_time=action_cond_data.duration_sec,
            slip_interval=action_cond_data.slip_interval,
            slip_damage_mod=action_cond_data.slip_damage_mod,
            max_stack_count=action_cond_data.max_stack_count,
            hit_attr_label=hit_data.hit_attr.id,
            action_cond_id=hit_data.hit_attr.action_condition_id
        )

    @staticmethod
    def to_debuff_unit(
            hit_data: HT, asset_action_condition: ActionConditionAsset
    ) -> list[ActionConditionEffectUnit]:
        """Get the debuff effect unit of ``hit_data``. Returns an empty list if not applicable."""
        if not hit_data.hit_attr.action_condition_id:
            # No action condition affiliated
            return []

        if not hit_data.target_simple == HitTargetSimple.ENEMY:
            # Target not enemy
            return []

        return AbilityConditionConverter.to_buffing_units(hit_data, asset_action_condition)

    @staticmethod
    def to_buffing_units(
            hit_data: HT, asset_action_condition: ActionConditionAsset
    ) -> list[ActionConditionEffectUnit]:
        """Converts ``hit_data`` to a list of buffing units as :class:`ActionConditionEffectUnit`."""
        units: list[Optional[ActionConditionEffectUnit]] = []

        # Get the action condition entry
        cond_entry: ActionConditionEntry = asset_action_condition.get_data_by_id(hit_data.hit_attr.action_condition_id)

        # --- Conditions in action condition

        units.append(AbilityConditionConverter.to_damage_self(hit_data.action_time, hit_data.hit_attr))

        # --- General buffs

        if cond_entry:
            # ATK
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.ATK, cond_entry.buff_atk, hit_data, cond_entry))
            # DEF
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.DEF, cond_entry.buff_def, hit_data, cond_entry))
            # CRT rate
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.CRT_RATE, cond_entry.buff_crt_rate, hit_data, cond_entry))
            # CRT damage
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.CRT_DAMAGE, cond_entry.buff_crt_damage, hit_data, cond_entry))
            # Skill damage
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.SKILL_DAMAGE, cond_entry.buff_skill_damage, hit_data, cond_entry))
            # FS damage
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.FS_DAMAGE, cond_entry.buff_fs_damage, hit_data, cond_entry))
            # ATK SPD
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.ATK_SPD, cond_entry.buff_atk_spd, hit_data, cond_entry))
            # FS SPD
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.FS_SPD, cond_entry.buff_fs_spd, hit_data, cond_entry))
            # SP rate
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.SP_RATE, cond_entry.buff_sp_rate, hit_data, cond_entry))

            # Damage Shield
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.SHIELD_SINGLE_DMG, cond_entry.shield_dmg, hit_data, cond_entry))
            # HP Shield
            units.append(AbilityConditionConverter.to_param_up(
                BuffParameter.SHIELD_LIFE, cond_entry.shield_hp, hit_data, cond_entry))

        # --- Instant gauge refill

        # SP charge %
        # idx 2 always give more accurate result (at least S!Cleo is giving the correct one)
        if skill_idx := SkillIndex(hit_data.hit_attr.sp_recov_skill_idx_2):
            if skill_idx == SkillIndex.S1:
                units.append(AbilityConditionConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S1, hit_data.hit_attr.sp_recov_ratio, hit_data, cond_entry))
            elif skill_idx == SkillIndex.S2:
                units.append(AbilityConditionConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S2, hit_data.hit_attr.sp_recov_ratio, hit_data, cond_entry))
            elif skill_idx == SkillIndex.USED_SKILL:
                units.append(AbilityConditionConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_USED, hit_data.hit_attr.sp_recov_ratio, hit_data, cond_entry))

        # Remove ``None`` element (``None`` will be added if the entry is ineffective)
        return list(sorted(u for u in units if u))
