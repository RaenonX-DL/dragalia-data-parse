"""Class for a single damaging hit."""
from dataclasses import dataclass, field

from dlparse.errors import BulletEndOfLifeError, DamagingHitValidationFailedError
from dlparse.mono.asset import ActionComponentHasHitLabels, ActionBullet
from .hit_base import HitData

__all__ = ("DamagingHitData",)


@dataclass
class DamagingHitData(HitData[ActionComponentHasHitLabels]):
    """Class for the data of a single damaging hit."""

    will_deteriorate: bool = field(init=False)
    deterioration_rate: float = 0
    max_hit_count: int = 0

    def _init_validity_check(self):
        if self.will_deteriorate and self.deterioration_rate == 0:
            # The hit ``will_deteriorate``, but the rate of deterioration is not set
            raise DamagingHitValidationFailedError("Deterioration rate not set, but the hit `will_deteriorate`")

    def __post_init__(self):
        self.will_deteriorate = \
            isinstance(self.action_component, ActionBullet) and self.action_component.will_deteriorate

        if isinstance(self.action_component, ActionBullet):
            self.deterioration_rate = self.action_component.attenuation_rate
            self.max_hit_count = self.action_component.max_hit_count

        self._init_validity_check()

    def damage_modifier_at_hit(self, hit_count: int) -> float:
        """
        Get the damage modifier at hit ``hit_count``.

        If the damage hit will not deteriorate, returns the original damage modifier.

        :raises BulletEndOfLifeError: if `hit_count` is beyond the maximum possible bullet hit count
        """
        # Early termination on non-deteriorating hits
        if not self.will_deteriorate:
            return self.hit_attr.damage_modifier

        # Raise error if beyond max hit count (if applicable)
        if self.max_hit_count and hit_count > self.max_hit_count:
            raise BulletEndOfLifeError(self.max_hit_count, hit_count)

        # - 1 for hit count here because the 1st hit deals the base damage (no deterioration)
        return self.hit_attr.damage_modifier * self.deterioration_rate ** (hit_count - 1)
