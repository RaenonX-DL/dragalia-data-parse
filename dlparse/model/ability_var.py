"""Classes for ability variant data."""
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from dlparse.enums import (
    AbilityUpParameter, AbilityVariantType, BuffParameter, Condition, ConditionComposite, HitTargetSimple, Status,
)
from dlparse.errors import AbilityVariantUnconvertibleError
from dlparse.mono.asset import AbilityEntry, AbilityVariantEntry, ActionConditionEntry
from .action_cond_conv import ActionCondEffectConvertPayload, ActionCondEffectConvertible
from .base import EffectUnitBase

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityVariantEffectUnit", "AbilityVariantEffectPayload", "AbilityVariantData", "ability_to_effect_units")


@dataclass(eq=False)
class AbilityVariantEffectUnit(EffectUnitBase):
    """The smallest unit of an ability effect coming from an ability variant."""

    source_ability_id: int
    condition_comp: ConditionComposite

    rate_max: float

    def __hash__(self):
        # x 1E5 for handling floating errors
        return hash((self.source_ability_id, self.parameter, int(self.rate * 1E5)))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return ((self.source_ability_id, self.condition_comp, int(self.parameter.value), self.rate)
                < (other.source_ability_id, other.condition_comp, int(other.parameter.value), other.rate))


@dataclass
class AbilityVariantEffectPayload(ActionCondEffectConvertPayload):
    """Payload object for variant effect conversion."""

    condition_comp: ConditionComposite
    source_ability_id: int


@dataclass
class AbilityVariantData(ActionCondEffectConvertible[AbilityVariantEffectUnit, AbilityVariantEffectPayload]):
    """An ability variant data class."""

    variant: AbilityVariantEntry

    type_enum: AbilityVariantType = field(init=False)

    def __post_init__(self):
        self.type_enum = AbilityVariantType(self.variant.type_id)

    def to_param_up(
            self, param_enum: BuffParameter, param_rate: float, action_cond: ActionConditionEntry,
            payload: AbilityVariantEffectPayload = None
    ) -> Optional[AbilityVariantEffectUnit]:
        if not param_rate:
            return None  # Rate is 0, parameter not raised

        return AbilityVariantEffectUnit(
            condition_comp=payload.condition_comp,
            source_ability_id=payload.source_ability_id,
            status=Status.NONE,
            target=HitTargetSimple.SELF,  # Effects of the ability from action condition should all targeted to self
            parameter=param_enum,
            probability_pct=action_cond.probability_pct,
            rate=param_rate,
            rate_max=0,
            max_stack_count=action_cond.max_stack_count,
            duration_time=action_cond.duration_sec,
            duration_count=action_cond.duration_count,
            slip_interval=action_cond.slip_interval,
            slip_damage_mod=action_cond.slip_damage_mod,
        )

    def to_affliction_unit(
            self, action_cond: "ActionConditionEntry",
            payload: AbilityVariantEffectPayload = None
    ) -> Optional[AbilityVariantEffectUnit]:
        return AbilityVariantEffectUnit(
            condition_comp=payload.condition_comp,
            source_ability_id=payload.source_ability_id,
            status=action_cond.afflict_status,
            target=HitTargetSimple.SELF,  # Effects of the ability from action condition should all targeted to self
            probability_pct=action_cond.probability_pct,
            rate=0,
            parameter=BuffParameter.AFFLICTION,
            duration_time=action_cond.duration_sec,
            duration_count=action_cond.duration_count,
            slip_interval=action_cond.slip_interval,
            slip_damage_mod=action_cond.slip_damage_mod,
            max_stack_count=action_cond.max_stack_count,
            rate_max=0
        )

    def _from_status_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        ability_param = AbilityUpParameter(self.variant.id_a)

        if ability_param == AbilityUpParameter.NONE:
            # Ability up is dummy (no effect), return an empty set
            # > This happens on Gala Leonidas AB1@Lv1 (1460), where the description only says
            # > "Leonidas only shapeshift to Mars." In this case, this serves as a dummy ability variant.
            return set()

        max_value = asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id, on_not_found=0)

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                parameter=ability_param.to_buff_parameter(),
                probability_pct=100,
                rate=self.variant.up_value / 100,  # Original data is percentage
                rate_max=max_value,
                target=HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            )
        }

    def _from_change_state(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return set(self.to_buff_units(asset_manager.asset_action_cond.get_data_by_id(self.variant.id_a), payload))

    def _from_sp_charge(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        charge_params = {
            BuffParameter.SP_CHARGE_PCT_S1, BuffParameter.SP_CHARGE_PCT_S2,
            BuffParameter.SP_CHARGE_PCT_S3, BuffParameter.SP_CHARGE_PCT_S4
        }

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                parameter=param,
                probability_pct=100,
                rate=self.variant.up_value / 100,  # Original data is percentage
                rate_max=asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id),
                target=HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            ) for param in charge_params
        }

    def to_effect_units(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        """
        Get the ability variant effect units of this ability variant.

        :raises AbilityVariantUnconvertibleError: if the variant type is not handled / unconvertible
        """
        if self.type_enum == AbilityVariantType.STATUS_UP:
            return self._from_status_up(asset_manager, payload)

        if self.type_enum == AbilityVariantType.CHANGE_STATE:
            return self._from_change_state(asset_manager, payload)

        if self.type_enum == AbilityVariantType.SP_CHARGE:
            return self._from_sp_charge(asset_manager, payload)

        raise AbilityVariantUnconvertibleError(payload.source_ability_id, self.variant.type_id)


def ability_to_effect_units(
        ability_entry: AbilityEntry, asset_manager: "AssetManager"
) -> set[AbilityVariantEffectUnit]:
    """Convert ``ability_entry`` to a set of variant effect units."""
    effect_units: set[AbilityVariantEffectUnit] = set()

    # Get the conditions
    conditions: list[Condition] = []
    if on_skill_cond := ability_entry.on_skill_condition:
        conditions.append(on_skill_cond)
    if ability_cond := ability_entry.condition.to_condition():
        conditions.append(ability_cond)

    # Get the variant payload
    payload = AbilityVariantEffectPayload(
        condition_comp=ConditionComposite(conditions),
        source_ability_id=ability_entry.id,
    )

    for variant in ability_entry.variants:
        if variant.type_enum == AbilityVariantType.OTHER_ABILITY:
            continue  # Refer to the other ability, no variant effect

        effect_units.update(AbilityVariantData(variant).to_effect_units(asset_manager, payload))

    return effect_units