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
            self.to_param_up(BuffParameter.CRT_RATE, action_cond.buff_crt_rate, action_cond, payload),
            # CRT damage
            self.to_param_up(BuffParameter.CRT_DAMAGE, action_cond.buff_crt_damage, action_cond, payload),
            # Skill damage
            self.to_param_up(BuffParameter.SKILL_DAMAGE, action_cond.buff_skill_damage, action_cond, payload),
            # FS damage
            self.to_param_up(BuffParameter.FS_DAMAGE, action_cond.buff_fs_damage, action_cond, payload, ),
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
            self.to_param_up(BuffParameter.SHIELD_SINGLE_DMG, action_cond.shield_dmg, action_cond, payload, ),
            # HP shield
            self.to_param_up(BuffParameter.SHIELD_LIFE, action_cond.shield_hp, action_cond, payload),

            # Flame resistance
            self.to_param_up(BuffParameter.RESISTANCE_FLAME, action_cond.resistance_flame, action_cond, payload),
            # Water resistance
            self.to_param_up(BuffParameter.RESISTANCE_WATER, action_cond.resistance_water, action_cond, payload),
            # Wind resistance
            self.to_param_up(BuffParameter.RESISTANCE_WIND, action_cond.resistance_wind, action_cond, payload),
            # Light resistance
            self.to_param_up(BuffParameter.RESISTANCE_LIGHT, action_cond.resistance_light, action_cond, payload),
            # Shadow resistance
            self.to_param_up(BuffParameter.RESISTANCE_SHADOW, action_cond.resistance_shadow, action_cond, payload)
        ]

    def _units_special_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[Optional[UT]]:
        return [
            # Energize
            self.to_param_up(BuffParameter.ENERGY_LEVEL, action_cond.energize_lv, action_cond, payload),
            # Inspire
            self.to_param_up(BuffParameter.INSPIRE_LEVEL, action_cond.inspire_lv, action_cond, payload),
        ]

    def to_buff_units(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None
    ) -> list[UT]:
        """Convert ``action_cond`` to a list of effect units."""
        return [
            unit for unit in
            self._units_common_buffs(action_cond, payload)
            + self._units_defensive_buffs(action_cond, payload)
            + self._units_special_buffs(action_cond, payload)
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
