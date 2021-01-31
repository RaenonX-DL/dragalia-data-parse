"""Extension to allow a hit data to convert itself to various effect units."""
from abc import ABC
from dataclasses import dataclass
from typing import Generic, Optional

from dlparse.enums import BuffParameter, HitTargetSimple, SkillIndex, Status
from dlparse.errors import UnhandledSelfDamageError
from dlparse.mono.asset import ActionBuffBomb, ActionConditionAsset, ActionConditionEntry, HitAttrEntry
from .action_cond_conv import ActionCondEffectConvertible
from .action_cond_effect import EnemyAfflictionEffectUnit, HitActionConditionEffectUnit
from .base import HitData, T

__all__ = ("HitDataEffectConvertible",)


@dataclass
class HitDataEffectConvertible(
    HitData, ActionCondEffectConvertible[HitActionConditionEffectUnit, None], Generic[T], ABC
):
    """Base hit data class which can be converted to various units."""

    def to_param_up(
            self, param_enum: BuffParameter, param_rate: float, action_cond: ActionConditionEntry,
            payload: None = None
    ) -> Optional[HitActionConditionEffectUnit]:
        """
        Create an effect unit (if applicable) based on the given action condition and the related data.

        If ``param_rate`` is ``0`` (meaning not used), ``None`` will be returned instead.

        if ``cond_entry`` is ``None``, both ``duration_sec`` and ``duration_count`` will set to 0.
        """
        if not param_rate:  # Param rate = 0 means not applicable
            return None

        return HitActionConditionEffectUnit(
            time=self.action_time,
            status=Status.NONE,
            target=self.target_simple,
            parameter=param_enum,
            probability_pct=action_cond.probability_pct,
            rate=param_rate,
            slip_interval_sec=action_cond.slip_interval_sec,
            slip_damage_mod=action_cond.slip_damage_mod,
            duration_sec=self.get_duration(action_cond),
            duration_count=action_cond.duration_count,
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.hit_attr.action_condition_id,
            max_stack_count=action_cond.max_stack_count
        )

    def to_affliction_unit(
            self, action_cond: ActionConditionEntry, payload: None = None
    ) -> Optional[EnemyAfflictionEffectUnit]:
        if not self.hit_attr.action_condition_id:
            # No action condition affiliated
            return None

        if self.target_simple != HitTargetSimple.ENEMY:
            # Target not enemy
            return None

        if not action_cond.afflict_status.is_abnormal_status:
            # Not afflicting action condition
            return None

        return EnemyAfflictionEffectUnit(
            time=self.action_component.time_start,
            status=action_cond.afflict_status,
            target=self.target_simple,
            probability_pct=action_cond.probability_pct,
            parameter=BuffParameter.AFFLICTION,
            duration_sec=action_cond.duration_sec,
            slip_interval_sec=action_cond.slip_interval_sec,
            slip_damage_mod=action_cond.slip_damage_mod,
            max_stack_count=action_cond.max_stack_count,
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.hit_attr.action_condition_id
        )

    def to_dispel_unit(
            self, param_enum: BuffParameter, action_cond: ActionConditionEntry, payload: None = None
    ) -> Optional[EnemyAfflictionEffectUnit]:
        return EnemyAfflictionEffectUnit(
            time=self.action_component.time_start,
            status=action_cond.afflict_status,
            target=self.target_simple,
            probability_pct=action_cond.probability_pct,
            parameter=BuffParameter.DISPEL,
            duration_sec=action_cond.duration_sec,
            slip_interval_sec=action_cond.slip_interval_sec,
            slip_damage_mod=action_cond.slip_damage_mod,
            max_stack_count=action_cond.max_stack_count,
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.hit_attr.action_condition_id
        )

    @staticmethod
    def to_damage_self(starting_time: float, hit_attr: HitAttrEntry) -> Optional[HitActionConditionEffectUnit]:
        """
        Return the corresponding :class:`HitActionConditionEffectUnit` if the hit attribute will self damage.

        Return ``None`` if not self damaging.

        :raises UnhandledSelfDamageError: if the self damage ability is unhandled
        """
        if not hit_attr.is_damage_self:
            return None

        if hit_attr.hp_fix_rate:
            return HitActionConditionEffectUnit(
                time=starting_time,
                status=Status.NONE,
                probability_pct=100,
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.HP_FIX_BY_MAX,
                rate=hit_attr.hp_fix_rate,
                slip_interval_sec=0,
                slip_damage_mod=0,
                duration_sec=0,
                duration_count=0,
                hit_attr_label=hit_attr.id,
                action_cond_id=hit_attr.action_condition_id,
                max_stack_count=0
            )

        if hit_attr.hp_consumption_rate:
            return HitActionConditionEffectUnit(
                time=starting_time,
                status=Status.NONE,
                probability_pct=100,
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.HP_DECREASE_BY_MAX,
                rate=hit_attr.hp_consumption_rate,
                slip_interval_sec=0,
                slip_damage_mod=0,
                duration_sec=0,
                duration_count=0,
                hit_attr_label=hit_attr.id,
                action_cond_id=hit_attr.action_condition_id,
                max_stack_count=0
            )

        raise UnhandledSelfDamageError(hit_attr.id)

    def to_marker_unit(self, asset_action_condition: ActionConditionAsset) -> list[HitActionConditionEffectUnit]:
        """Get the marker effect of ``hit_data`` (if any) as a debuff unit."""
        if not isinstance(self.action_component, ActionBuffBomb):
            return []

        action_cond: ActionConditionEntry = asset_action_condition.get_data_by_id(
            self.action_component.action_condition_id
        )

        return [HitActionConditionEffectUnit(
            time=self.action_time,
            status=Status.NONE,
            probability_pct=action_cond.probability_pct,
            target=HitTargetSimple.ENEMY,
            parameter=BuffParameter.MARK,
            rate=0,
            slip_interval_sec=action_cond.slip_interval_sec,
            slip_damage_mod=action_cond.slip_damage_mod,
            duration_sec=action_cond.duration_sec,
            duration_count=action_cond.duration_count,
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.action_component.action_condition_id,
            max_stack_count=1
        )]

    def to_debuff_units(
            self, asset_action_condition: ActionConditionAsset
    ) -> list[HitActionConditionEffectUnit]:
        """Get the debuff effect unit of ``hit_data``. Return an empty list if not applicable."""
        if self.target_simple != HitTargetSimple.ENEMY:
            # Target not enemy
            return []

        ret: list[HitActionConditionEffectUnit] = []

        # Action is buff bomb - mark of Nobunaga S1 (`102501031`)
        ret.extend(self.to_marker_unit(asset_action_condition))

        if not ret and not self.hit_attr.action_condition_id:
            # No marker units and action condition affiliated to the hit data
            return []

        # Add all buffing/debuffing units
        ret.extend(self.to_buffing_units(asset_action_condition))

        return ret

    def to_buffing_units(
            self, asset_action_condition: ActionConditionAsset
    ) -> list[HitActionConditionEffectUnit]:
        """Converts ``hit_data`` to a list of buffing units as :class:`HitActionConditionEffectUnit`."""
        units: list[Optional[HitActionConditionEffectUnit]] = []

        # Get the action condition entry
        action_cond: ActionConditionEntry = asset_action_condition.get_data_by_id(self.hit_attr.action_condition_id)

        # --- Conditions in action condition

        units.append(self.to_damage_self(self.action_time, self.hit_attr))

        # --- General buffs

        if action_cond:
            units.extend(self.to_effect_units(action_cond))

        # --- Instant gauge refill

        # SP charge %
        # idx 2 always give more accurate result (at least S!Cleo is giving the correct one)
        if skill_idx := SkillIndex(self.hit_attr.sp_recov_skill_idx_2):
            if skill_idx == SkillIndex.S1:
                units.append(self.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S1, self.hit_attr.sp_recov_ratio, action_cond
                ))
            elif skill_idx == SkillIndex.S2:
                units.append(self.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S2, self.hit_attr.sp_recov_ratio, action_cond
                ))
            elif skill_idx == SkillIndex.USED_SKILL:
                units.append(self.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_USED, self.hit_attr.sp_recov_ratio, action_cond
                ))

        # Remove ``None`` element (``None`` will be added if the entry is ineffective)
        return list(sorted(u for u in units if u))
