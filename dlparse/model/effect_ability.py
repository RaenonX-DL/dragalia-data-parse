"""Class for an ability effect unit."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from dlparse.enums import (
    AbilityUpParameter, AbilityVariantType, BuffParameter, ConditionComposite, HitTargetSimple, Status,
)
from dlparse.errors import AbilityVariantUnconvertibleError
from .effect_base import EffectUnitBase

if TYPE_CHECKING:
    from dlparse.mono.asset import AbilityLimitGroupAsset, AbilityVariantEntry

__all__ = ("AbilityVariantEffectUnit",)


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

    @staticmethod
    def _from_status_up(
            ability_variant: "AbilityVariantEntry", ability_id: int, condition_comp: ConditionComposite, /,
            asset_ability_limit: "AbilityLimitGroupAsset"
    ) -> set["AbilityVariantEffectUnit"]:
        return {
            AbilityVariantEffectUnit(
                source_ability_id=ability_id,
                condition_comp=condition_comp,
                parameter=AbilityUpParameter(ability_variant.id_a).to_buff_parameter(),
                probability_pct=100,
                rate=ability_variant.up_value / 100,  # Original data is percentage
                rate_max=asset_ability_limit.get_max_value(ability_variant.limited_group_id),
                target=HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            )
        }

    @staticmethod
    def _from_sp_charge(
            ability_variant: "AbilityVariantEntry", ability_id: int, condition_comp: ConditionComposite, /,
            asset_ability_limit: "AbilityLimitGroupAsset"
    ) -> set["AbilityVariantEffectUnit"]:
        charge_params = {
            BuffParameter.SP_CHARGE_PCT_S1, BuffParameter.SP_CHARGE_PCT_S2,
            BuffParameter.SP_CHARGE_PCT_S3, BuffParameter.SP_CHARGE_PCT_S4
        }

        return {
            AbilityVariantEffectUnit(
                source_ability_id=ability_id,
                condition_comp=condition_comp,
                parameter=param,
                probability_pct=100,
                rate=ability_variant.up_value / 100,  # Original data is percentage
                rate_max=asset_ability_limit.get_max_value(ability_variant.limited_group_id),
                target=HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            ) for param in charge_params
        }

    @classmethod
    def from_ability_variant(
            cls, ability_variant: "AbilityVariantEntry", ability_id: int, condition_comp: ConditionComposite, /,
            asset_ability_limit: "AbilityLimitGroupAsset"
    ) -> set["AbilityVariantEffectUnit"]:
        """
        Get the ability variant effect units of this ability variant.

        :raises AbilityVariantUnconvertibleError: if the variant type is not handled / unconvertible
        """
        if ability_variant.type_enum == AbilityVariantType.STATUS_UP:
            return cls._from_status_up(
                ability_variant, ability_id, condition_comp,
                asset_ability_limit=asset_ability_limit
            )

        if ability_variant.type_enum == AbilityVariantType.SP_CHARGE:
            return cls._from_sp_charge(
                ability_variant, ability_id, condition_comp,
                asset_ability_limit=asset_ability_limit
            )

        raise AbilityVariantUnconvertibleError(ability_id, ability_variant.type_id)
