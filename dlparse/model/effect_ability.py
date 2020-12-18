"""Class for an ability effect unit."""
from dataclasses import dataclass

from dlparse.enums import ConditionComposite
from .effect_base import EffectUnitBase

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
