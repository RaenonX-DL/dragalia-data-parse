"""Class for a single damaging hit."""
from dataclasses import dataclass

from dlparse.errors import BulletEndOfLifeError, DamagingHitValidationFailedError
from dlparse.mono.asset import ActionComponentHasHitLabels, ActionBullet, ActionBuffField, ActionBulletStockFire
from .hit_base import HitData

__all__ = ("DamagingHitData",)


@dataclass
class DamagingHitData(HitData[ActionComponentHasHitLabels]):
    """Class for the data of a single damaging hit."""

    # region Bullet deterioration
    will_deteriorate: bool = False
    deterioration_rate: float = 0
    max_hit_count: int = 0
    # endregion

    # region Damage modifiers when inside the buff zones
    mod_on_self_buff_zone: float = 0
    mod_on_ally_buff_zone: float = 0
    # endregion

    # region Buff count dependent bullets
    is_user_buff_count_dependent: bool = False

    # endregion

    def _init_validity_check(self):
        if self.will_deteriorate and self.deterioration_rate == 0:
            # The hit ``will_deteriorate``, but the rate of deterioration is not set
            raise DamagingHitValidationFailedError("Deterioration rate not set, but the hit `will_deteriorate`")

    def __post_init__(self):
        # General bullet setting copy
        if isinstance(self.action_component, ActionBullet):
            self.will_deteriorate = self.action_component.will_deteriorate
            self.deterioration_rate = self.action_component.attenuation_rate

            if isinstance(self.action_component, ActionBulletStockFire):
                # Check if the damaging hit depends on user buff count
                self.is_user_buff_count_dependent = self.action_component.is_user_buff_count_dependent

            # Set the max hit count except for buff depending hits which max hit count depends on the other conditions
            if not self.is_user_buff_count_dependent:
                self.max_hit_count = self.action_component.max_hit_count

        # Buff zone specific damage mod
        if isinstance(self.action_component, ActionBuffField):
            if self.action_component.count_for_self_built:
                self.mod_on_self_buff_zone = self.hit_attr.damage_modifier
            else:
                self.mod_on_ally_buff_zone = self.hit_attr.damage_modifier

        self._init_validity_check()

    @property
    def is_effective_inside_buff_zone(self) -> bool:
        """Check if the hit is only effective if the user is inside buff zones."""
        return bool(self.mod_on_self_buff_zone or self.mod_on_ally_buff_zone)

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

    def mods_in_self_buff_zone(self, count: int) -> list[float]:
        """Get the damage modifiers if standing on ``count`` buff zones created by the user."""
        return [self.mod_on_self_buff_zone] * count

    def mods_in_ally_buff_zone(self, count: int) -> list[float]:
        """Get the damage modifiers if standing on ``count`` buff zones created by the allies."""
        return [self.mod_on_ally_buff_zone] * count
