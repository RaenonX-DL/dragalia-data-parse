"""Extension to allow a hit data to convert itself to various effect units."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TYPE_CHECKING, TypeVar

from dlparse.enums import BuffParameter, ConditionComposite
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
            payload: Optional[PT] = None, additional_conditions: Optional[ConditionComposite] = None
    ) -> Optional[UT]:
        """Create an effect unit (if applicable) based on the given action condition and the related data."""
        raise NotImplementedError()

    def _units_common_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None,
            additional_conditions: Optional[ConditionComposite] = None
    ) -> list[Optional[UT]]:
        return [
            # ATK
            self.to_param_up(
                BuffParameter.ATK_BUFF, action_cond.buff_atk, action_cond, payload, additional_conditions
            ),
            # DEF & DEF (B) - I don't know why the fuck they need two of this
            self.to_param_up(
                BuffParameter.DEF_BUFF, action_cond.buff_def + action_cond.buff_def_b, action_cond, payload,
                additional_conditions
            ),
            # CRT rate
            self.to_param_up(
                BuffParameter.CRT_RATE, action_cond.buff_crt_rate, action_cond, payload,
                additional_conditions
            ),
            # CRT damage
            self.to_param_up(
                BuffParameter.CRT_DAMAGE, action_cond.buff_crt_damage, action_cond, payload,
                additional_conditions
            ),
            # Skill damage
            self.to_param_up(
                BuffParameter.SKILL_DAMAGE, action_cond.buff_skill_damage, action_cond, payload,
                additional_conditions
            ),
            # FS damage
            self.to_param_up(
                BuffParameter.FS_DAMAGE, action_cond.buff_fs_damage, action_cond, payload,
                additional_conditions
            ),
            # ATK SPD
            self.to_param_up(
                BuffParameter.ATK_SPD, action_cond.buff_atk_spd, action_cond, payload,
                additional_conditions
            ),
            # FS SPD
            self.to_param_up(
                BuffParameter.FS_SPD, action_cond.buff_fs_spd, action_cond, payload,
                additional_conditions),
            # SP rate
            self.to_param_up(
                BuffParameter.SP_RATE, action_cond.buff_sp_rate, action_cond, payload,
                additional_conditions
            )
        ]

    def _units_defensive_buffs(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None,
            additional_conditions: Optional[ConditionComposite] = None
    ) -> list[Optional[UT]]:
        return [
            # Damage shield
            self.to_param_up(
                BuffParameter.SHIELD_SINGLE_DMG, action_cond.shield_dmg, action_cond, payload,
                additional_conditions
            ),
            # HP shield
            self.to_param_up(
                BuffParameter.SHIELD_LIFE, action_cond.shield_hp, action_cond, payload,
                additional_conditions
            ),

            # Flame resistance
            self.to_param_up(
                BuffParameter.RESISTANCE_FLAME, action_cond.resistance_flame, action_cond, payload,
                additional_conditions
            ),
            # Water resistance
            self.to_param_up(
                BuffParameter.RESISTANCE_WATER, action_cond.resistance_water, action_cond, payload,
                additional_conditions
            ),
            # Wind resistance
            self.to_param_up(
                BuffParameter.RESISTANCE_WIND, action_cond.resistance_wind, action_cond, payload,
                additional_conditions
            ),
            # Light resistance
            self.to_param_up(
                BuffParameter.RESISTANCE_LIGHT, action_cond.resistance_light, action_cond, payload,
                additional_conditions
            ),
            # Shadow resistance
            self.to_param_up(
                BuffParameter.RESISTANCE_SHADOW, action_cond.resistance_shadow, action_cond, payload,
                additional_conditions
            )
        ]

    def to_buff_units(
            self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None,
            additional_conditions: Optional[ConditionComposite] = None
    ) -> list[UT]:
        """Convert ``action_cond`` to a list of effect units."""
        return [
            unit for unit in
            self._units_common_buffs(action_cond, payload, additional_conditions)
            + self._units_defensive_buffs(action_cond, payload, additional_conditions)
            if unit  # Skipping empty unit
        ]

    @abstractmethod
    def to_affliction_unit(self, action_cond: "ActionConditionEntry", payload: Optional[PT] = None) -> Optional[UT]:
        """Get the affliction effect unit of ``action_cond``."""
        raise NotImplementedError()
