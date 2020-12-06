"""Class for a single damaging hit."""
from dataclasses import dataclass
from typing import Optional

from dlparse.errors import BulletEndOfLifeError, DamagingHitValidationFailedError
from dlparse.mono.asset import (
    ActionBuffField, ActionBullet, ActionBulletStockFire, ActionComponentHasHitLabels, ActionConditionAsset,
)
from .hit_base import HitData
from .skill_affliction import SkillAfflictionUnit

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

    # region Flags of bullets having special patterns
    is_depends_on_user_buff_count: bool = False
    is_depends_on_bullet_on_map: bool = False

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
                # Check if the damaging hit depends on special pattern
                self.is_depends_on_user_buff_count = self.action_component.is_depends_on_user_buff_count
                self.is_depends_on_bullet_on_map = self.action_component.is_depends_on_bullet_on_map

            # Set the max hit count except for special pattern bullets
            if not (isinstance(self.action_component, ActionBulletStockFire)
                    and self.action_component.is_special_pattern):
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

    def to_affliction_unit(self, asset_action_condition: ActionConditionAsset) -> Optional[SkillAfflictionUnit]:
        """Get the affliction unit of this hit data."""
        if not self.hit_attr.action_condition_id:
            # No action condition affiliated
            return None

        action_cond_data = asset_action_condition.get_data_by_id(self.hit_attr.action_condition_id)

        if not action_cond_data.afflict_status.is_abnormal_status:
            # Not afflicting action condition
            return None

        return SkillAfflictionUnit(
            status=action_cond_data.afflict_status,
            time=self.action_component.time_start,
            rate_percent=action_cond_data.probability_pct,
            duration=action_cond_data.duration_sec,
            interval=action_cond_data.slip_interval,
            damage_mod=action_cond_data.slip_damage_mod,
            stackable=True,  # FIXME: OG!Alex DEF down?
            hit_attr_label=self.hit_attr.id,
            action_cond_id=self.hit_attr.action_condition_id
        )
