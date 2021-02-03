"""Extension to allow a hit data to convert itself to various effect units."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TYPE_CHECKING, TypeVar

from dlparse.enums import BuffParameter
from .base import EffectUnitBase

if TYPE_CHECKING:
    from dlparse.mono.asset import ActionConditionEntry

__all__ = ("ActionCondEffectConvertible", "ActionCondEffectConvertPayload")

UT = TypeVar("UT", bound=EffectUnitBase)


@dataclass
class ActionCondEffectConvertPayload(ABC):
    """Base class for the action condition conversion payload."""


PT = TypeVar("PT", bound=ActionCondEffectConvertPayload)


@dataclass
class ActionCondEffectConvertible(Generic[UT, PT], ABC):
    """Base data class which provides methods for converting action condition to effect units."""

    @abstractmethod
    def to_param_up(
            self, param_enum: BuffParameter, param_rate: float, action_cond: "ActionConditionEntry",
            payload: Optional[PT] = None
    ) -> Optional[UT]:
        """Create an effect unit (if applicable) based on the given action condition and the related data."""
        raise NotImplementedError()

    @abstractmethod
    def to_affliction_unit(self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None) -> Optional[UT]:
        """Get the affliction effect unit of ``action_cond``."""
        raise NotImplementedError()

    @abstractmethod
    def to_dispel_unit(
            self, param_enum: BuffParameter, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> Optional[UT]:
        """Create an effect unit (if applicable) that represents the effect of dispel."""
        raise NotImplementedError()

    def _units_common_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[Optional[UT]]:
        return [
            # ATK
            self.to_param_up(BuffParameter.ATK_BUFF, action_cond.buff_atk, action_cond, payload),
            # DEF & DEF (B) - I don't know why the fuck they need two of this
            self.to_param_up(
                BuffParameter.DEF_BUFF, action_cond.buff_def + action_cond.buff_def_b, action_cond, payload
            ),
            # CRT rate
            self.to_param_up(BuffParameter.CRT_RATE_BUFF, action_cond.buff_crt_rate, action_cond, payload),
            # CRT damage
            self.to_param_up(BuffParameter.CRT_DAMAGE_BUFF, action_cond.buff_crt_damage, action_cond, payload),
            # Skill damage
            self.to_param_up(BuffParameter.SKILL_DAMAGE_BUFF, action_cond.buff_skill_damage, action_cond, payload),
            # FS damage
            self.to_param_up(BuffParameter.FS_DAMAGE_BUFF, action_cond.buff_fs_damage, action_cond, payload, ),
            # ATK SPD
            self.to_param_up(BuffParameter.ASPD_BUFF, action_cond.buff_atk_spd, action_cond, payload),
            # FS SPD
            self.to_param_up(BuffParameter.FS_SPD, action_cond.buff_fs_spd, action_cond, payload),
            # SP rate
            self.to_param_up(BuffParameter.SP_RATE, action_cond.buff_sp_rate, action_cond, payload)
        ]

    def _units_defensive_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[Optional[UT]]:
        return [
            # Damage shield
            self.to_param_up(BuffParameter.SHIELD_SINGLE_DMG, action_cond.shield_dmg, action_cond, payload),
            # HP shield
            self.to_param_up(BuffParameter.SHIELD_LIFE, action_cond.shield_hp, action_cond, payload),

            # Damage reduction
            self.to_param_up(BuffParameter.DAMAGE_REDUCTION, action_cond.damage_reduction, action_cond, payload),

            # Flame resistance
            self.to_param_up(BuffParameter.RESISTANCE_FLAME_BUFF, action_cond.resistance_flame, action_cond, payload),
            # Water resistance
            self.to_param_up(BuffParameter.RESISTANCE_WATER_BUFF, action_cond.resistance_water, action_cond, payload),
            # Wind resistance
            self.to_param_up(BuffParameter.RESISTANCE_WIND_BUFF, action_cond.resistance_wind, action_cond, payload),
            # Light resistance
            self.to_param_up(BuffParameter.RESISTANCE_LIGHT_BUFF, action_cond.resistance_light, action_cond, payload),
            # Shadow resistance
            self.to_param_up(BuffParameter.RESISTANCE_SHADOW_BUFF, action_cond.resistance_shadow, action_cond, payload)
        ]

    def _units_recovery_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[Optional[UT]]:
        ret = []

        # Heal/Damage over time
        if action_cond.slip_damage_hp_rate < 0:
            # HoT
            ret.append(self.to_param_up(
                BuffParameter.HEAL_OVER_TIME_HP, -action_cond.slip_damage_hp_rate, action_cond, payload
            ))
        elif action_cond.slip_damage_hp_rate < 0:
            # DoT
            ret.append(self.to_param_up(
                BuffParameter.DAMAGE_OVER_TIME_HP, action_cond.slip_damage_hp_rate, action_cond, payload
            ))

        if action_cond.regen_rp:
            ret.append(self.to_param_up(
                BuffParameter.HEAL_OVER_TIME_RP, action_cond.regen_rp / 100, action_cond, payload
            ))

        return ret

    def _units_special_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[Optional[UT]]:
        return [
            # Energize
            self.to_param_up(BuffParameter.ENERGY_LEVEL, action_cond.energize_lv, action_cond, payload),
            # Inspire
            self.to_param_up(BuffParameter.INSPIRE_LEVEL, action_cond.inspire_lv, action_cond, payload),
            # HP Drain
            self.to_param_up(BuffParameter.HP_DRAIN_DAMAGE, action_cond.hp_drain_rate, action_cond, payload),
        ]

    def _units_resistance_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[Optional[UT]]:
        return [
            self.to_param_up(
                BuffParameter.RESISTANCE_POISON, action_cond.resistance_poison, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_BURN, action_cond.resistance_burn, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_FREEZE, action_cond.resistance_freeze, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_PARALYZE, action_cond.resistance_paralyze, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_BLIND, action_cond.resistance_blind, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_STUN, action_cond.resistance_stun, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_CURSE, action_cond.resistance_curse, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_BOG, action_cond.resistance_bog, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_SLEEP, action_cond.resistance_sleep, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_FROSTBITE, action_cond.resistance_frostbite, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_FLASHBURN, action_cond.resistance_flashburn, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_STORMLASH, action_cond.resistance_stormlash, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_SHADOWBLIGHT, action_cond.resistance_shadowblight, action_cond, payload
            ),
            self.to_param_up(
                BuffParameter.RESISTANCE_SCORCHREND, action_cond.resistance_scorchrend, action_cond, payload
            ),
        ]

    def to_effect_units(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[UT]:
        """Convert ``action_cond`` to a list of effect units."""
        return [
            unit for unit in
            self._units_common_buffs(action_cond, payload)
            + self._units_defensive_buffs(action_cond, payload)
            + self._units_recovery_buffs(action_cond, payload)
            + self._units_special_buffs(action_cond, payload)
            + self._units_resistance_buffs(action_cond, payload)
            if unit  # Skipping empty unit
        ]

    def to_dispel_units(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[Optional[UT]]:
        """Convert ``action_cond`` to a list of buff dispel units."""
        if not action_cond.is_dispel_buff:
            return []

        if dispel_unit := self.to_dispel_unit(BuffParameter.DISPEL, action_cond, payload):
            return [dispel_unit]

        return []
