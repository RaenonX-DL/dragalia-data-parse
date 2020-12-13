"""Extension to allow a hit data to convert itself to various effect units."""
from abc import ABC
from dataclasses import dataclass
from typing import Generic, Optional

from dlparse.enums import BuffParameter, HitTargetSimple, SkillIndex, Status
from dlparse.errors import UnhandledSelfDamageError
from dlparse.mono.asset import ActionBuffBomb, ActionConditionAsset, ActionConditionEntry, HitAttrEntry
from .effect_action_cond import ActionConditionEffectUnit, AfflictionEffectUnit
from .hit_base import HitData, T

__all__ = ("UnitsConvertibleHitData",)


@dataclass
class UnitsConvertibleHitData(HitData, Generic[T], ABC):
    """Base hit data class which can be converted to various units."""

    def to_param_up(
            self, param_enum: BuffParameter, param_rate: float, cond_entry: Optional[ActionConditionEntry]
    ) -> Optional[ActionConditionEffectUnit]:
        """
        Creates an effect unit (if applicable) based on the given data.

        If ``param_rate`` is ``0`` (meaning not used), ``None`` will be returned instead.

        if ``cond_entry`` is ``None``, both ``duration_time`` and ``duration_count`` will set to 0.
        """
        if not param_rate:  # Param rate = 0 means not applicable
            return None

        return ActionConditionEffectUnit(
            time=self.action_time,
            status=Status.NONE,
            target=self.target_simple,
            parameter=param_enum,
            probability_pct=cond_entry.probability_pct if cond_entry else 0,
            rate=param_rate,
            slip_interval=cond_entry.slip_interval if cond_entry else 0,
            slip_damage_mod=cond_entry.slip_damage_mod if cond_entry else 0,
            duration_time=self.get_duration(cond_entry),
            duration_count=cond_entry.duration_count if cond_entry else 0,
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.hit_attr.action_condition_id,
            max_stack_count=cond_entry.max_stack_count if cond_entry else 0
        )

    @staticmethod
    def to_damage_self(starting_time: float, hit_attr: HitAttrEntry) -> Optional[ActionConditionEffectUnit]:
        """
        Return the corresponding :class:`ActionConditionEffectUnit` if the hit attribute will self damage.

        Return ``None`` if not self damaging.

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

    def to_marker_unit(self, asset_action_condition: ActionConditionAsset) -> list[ActionConditionEffectUnit]:
        """Get the marker effect of ``hit_data`` (if any) as a debuff unit."""
        if not isinstance(self.action_component, ActionBuffBomb):
            return []

        action_cond: ActionConditionEntry = asset_action_condition.get_data_by_id(
            self.action_component.action_condition_id
        )

        return [ActionConditionEffectUnit(
            time=self.action_time,
            status=Status.NONE,
            probability_pct=action_cond.probability_pct,
            target=HitTargetSimple.ENEMY,
            parameter=BuffParameter.MARK,
            rate=0,
            slip_interval=action_cond.slip_interval,
            slip_damage_mod=action_cond.slip_damage_mod,
            duration_time=action_cond.duration_sec,
            duration_count=action_cond.duration_count,
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.action_component.action_condition_id,
            max_stack_count=1
        )]

    def to_affliction_unit(
            self, asset_action_condition: ActionConditionAsset
    ) -> Optional[AfflictionEffectUnit]:
        """Get the affliction effect unit of ``hit_data``. Return ``None`` if not applicable."""
        if not self.hit_attr.action_condition_id:
            # No action condition affiliated
            return None

        if self.target_simple != HitTargetSimple.ENEMY:
            # Target not enemy
            return None

        action_cond_data = asset_action_condition.get_data_by_id(self.hit_attr.action_condition_id)

        if not action_cond_data.afflict_status.is_abnormal_status:
            # Not afflicting action condition
            return None

        return AfflictionEffectUnit(
            time=self.action_component.time_start,
            status=action_cond_data.afflict_status,
            target=self.target_simple,
            probability_pct=action_cond_data.probability_pct,
            parameter=BuffParameter.AFFLICTION,
            duration_time=action_cond_data.duration_sec,
            slip_interval=action_cond_data.slip_interval,
            slip_damage_mod=action_cond_data.slip_damage_mod,
            max_stack_count=action_cond_data.max_stack_count,
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.hit_attr.action_condition_id
        )

    def to_debuff_units(
            self, asset_action_condition: ActionConditionAsset
    ) -> list[ActionConditionEffectUnit]:
        """Get the debuff effect unit of ``hit_data``. Return an empty list if not applicable."""
        if self.target_simple != HitTargetSimple.ENEMY:
            # Target not enemy
            return []

        ret: list[ActionConditionEffectUnit] = []

        # Action is buff bomb - mark of Nobunaga S1 (`102501031`)
        ret.extend(self.to_marker_unit(asset_action_condition))

        if not ret and not self.hit_attr.action_condition_id:
            # No marker units and action condition affiliated to the hit data
            return []

        # Add all buffing/debuffing units
        ret.extend(self.to_buffing_units(asset_action_condition))

        return ret

    def _units_common_buffs(
            self, cond_entry: ActionConditionEntry
    ) -> list[Optional[ActionConditionEffectUnit]]:
        return [
            # ATK
            self.to_param_up(BuffParameter.ATK, cond_entry.buff_atk, cond_entry),
            # DEF
            self.to_param_up(BuffParameter.DEF, cond_entry.buff_def, cond_entry),
            # CRT rate
            self.to_param_up(BuffParameter.CRT_RATE, cond_entry.buff_crt_rate, cond_entry),
            # CRT damage
            self.to_param_up(BuffParameter.CRT_DAMAGE, cond_entry.buff_crt_damage, cond_entry),
            # Skill damage
            self.to_param_up(BuffParameter.SKILL_DAMAGE, cond_entry.buff_skill_damage, cond_entry),
            # FS damage
            self.to_param_up(BuffParameter.FS_DAMAGE, cond_entry.buff_fs_damage, cond_entry),
            # ATK SPD
            self.to_param_up(BuffParameter.ATK_SPD, cond_entry.buff_atk_spd, cond_entry),
            # FS SPD
            self.to_param_up(BuffParameter.FS_SPD, cond_entry.buff_fs_spd, cond_entry),
            # SP rate
            self.to_param_up(BuffParameter.SP_RATE, cond_entry.buff_sp_rate, cond_entry)
        ]

    def _units_defensive_buffs(
            self, cond_entry: ActionConditionEntry
    ) -> list[Optional[ActionConditionEffectUnit]]:
        return [
            # Damage shield
            self.to_param_up(BuffParameter.SHIELD_SINGLE_DMG, cond_entry.shield_dmg, cond_entry),
            # HP shield
            self.to_param_up(BuffParameter.SHIELD_LIFE, cond_entry.shield_hp, cond_entry),

            # Flame resistance
            self.to_param_up(BuffParameter.RESISTANCE_FLAME, cond_entry.resistance_flame, cond_entry),
            # Water resistance
            self.to_param_up(BuffParameter.RESISTANCE_WATER, cond_entry.resistance_water, cond_entry),
            # Wind resistance
            self.to_param_up(BuffParameter.RESISTANCE_WIND, cond_entry.resistance_wind, cond_entry),
            # Light resistance
            self.to_param_up(BuffParameter.RESISTANCE_LIGHT, cond_entry.resistance_light, cond_entry),
            # Shadow resistance
            self.to_param_up(BuffParameter.RESISTANCE_SHADOW, cond_entry.resistance_shadow, cond_entry)
        ]

    def to_buffing_units(
            self, asset_action_condition: ActionConditionAsset
    ) -> list[ActionConditionEffectUnit]:
        """Converts ``hit_data`` to a list of buffing units as :class:`ActionConditionEffectUnit`."""
        units: list[Optional[ActionConditionEffectUnit]] = []

        # Get the action condition entry
        cond_entry: ActionConditionEntry = asset_action_condition.get_data_by_id(self.hit_attr.action_condition_id)

        # --- Conditions in action condition

        units.append(self.to_damage_self(self.action_time, self.hit_attr))

        # --- General buffs

        if cond_entry:
            units.extend(self._units_common_buffs(cond_entry))
            units.extend(self._units_defensive_buffs(cond_entry))

        # --- Instant gauge refill

        # SP charge %
        # idx 2 always give more accurate result (at least S!Cleo is giving the correct one)
        if skill_idx := SkillIndex(self.hit_attr.sp_recov_skill_idx_2):
            if skill_idx == SkillIndex.S1:
                units.append(self.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S1, self.hit_attr.sp_recov_ratio, cond_entry
                ))
            elif skill_idx == SkillIndex.S2:
                units.append(self.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S2, self.hit_attr.sp_recov_ratio, cond_entry
                ))
            elif skill_idx == SkillIndex.USED_SKILL:
                units.append(self.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_USED, self.hit_attr.sp_recov_ratio, cond_entry
                ))

        # Remove ``None`` element (``None`` will be added if the entry is ineffective)
        return list(sorted(u for u in units if u))
