"""Classes that allow ability variants to be converted into effect units."""
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from dlparse.enums import (
    AbilityUpParameter, AbilityVariantType, BuffParameter, ConditionComposite, HitTargetSimple, Status,
)
from dlparse.errors import AbilityVariantUnconvertibleError
from .action_cond_conv import ActionCondEffectConvertPayload, ActionCondEffectConvertible
from .effect_ability import AbilityVariantEffectUnit

if TYPE_CHECKING:
    from dlparse.mono.asset import ActionConditionEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityVariantEffectPayload", "AbilityVariantEffectConvertible")


@dataclass
class AbilityVariantEffectPayload(ActionCondEffectConvertPayload):
    """Payload object for variant effect conversion."""

    condition_comp: ConditionComposite
    source_ability_id: int


@dataclass
class AbilityVariantEffectConvertible(
    ActionCondEffectConvertible[AbilityVariantEffectUnit, AbilityVariantEffectPayload]
):
    """Class that allows the ability variant to be converted into effect units."""

    type_id: int
    id_a: int
    id_b: int
    id_c: int
    id_str: str
    limited_group_id: int
    target_action_id: int
    up_value: float

    type_enum: AbilityVariantType = field(init=False)

    def __post_init__(self):
        self.type_enum = AbilityVariantType(self.type_id)

    def to_param_up(
            self, param_enum: BuffParameter, param_rate: float, action_cond: "ActionConditionEntry",
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
    ) -> set["AbilityVariantEffectUnit"]:
        ability_param = AbilityUpParameter(self.id_a)

        if ability_param == AbilityUpParameter.NONE:
            # Ability up is dummy (no effect), return an empty set
            # > This happens on Gala Leonidas AB1@Lv1 (1460), where the description only says
            # > "Leonidas only shapeshift to Mars." In this case, this serves as a dummy ability variant.
            return set()

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                parameter=ability_param.to_buff_parameter(),
                probability_pct=100,
                rate=self.up_value / 100,  # Original data is percentage
                rate_max=asset_manager.asset_ability_limit.get_max_value(self.limited_group_id, on_not_found=0),
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
    ) -> set["AbilityVariantEffectUnit"]:
        return set(self.to_buff_units(asset_manager.asset_action_cond.get_data_by_id(self.id_a), payload))

    def _from_sp_charge(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set["AbilityVariantEffectUnit"]:
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
                rate=self.up_value / 100,  # Original data is percentage
                rate_max=asset_manager.asset_ability_limit.get_max_value(self.limited_group_id),
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
    ) -> set["AbilityVariantEffectUnit"]:
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

        raise AbilityVariantUnconvertibleError(payload.source_ability_id, self.type_id)
