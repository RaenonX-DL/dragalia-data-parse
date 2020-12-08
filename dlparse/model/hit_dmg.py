"""Class for a single damaging hit."""
from dataclasses import dataclass
from typing import Optional

from dlparse.enums import SkillConditionCategories, SkillConditionComposite
from dlparse.errors import AppValueError, BulletEndOfLifeError, DamagingHitValidationFailedError
from dlparse.mono.asset import (
    ActionBuffField, ActionBullet, ActionBulletStockFire, ActionComponentHasHitLabels, ActionConditionAsset,
    PlayerActionInfoAsset,
)
from dlparse.utils import AbilityConditionConverter, calculate_crisis_mod
from .effect_action_cond import ActionConditionEffectUnit, AfflictionEffectUnit
from .hit_base import HitData

__all__ = ("DamagingHitData", "DamageUnit")


@dataclass
class DamageUnit:
    """Class for a single actual damage hit."""

    mod: float
    unit_affliction: Optional[AfflictionEffectUnit]
    unit_debuffs: list[ActionConditionEffectUnit]
    hit_attr_label: str

    def __post_init__(self):
        if self.unit_affliction and not isinstance(self.unit_affliction, AfflictionEffectUnit):
            raise AppValueError(f"Unexpected affliction unit type {type(self.unit_affliction)}")

    @property
    def is_empty(self) -> bool:
        """Check if the damage unit is empty. Empty here means that the mod is ``0`` and both units are ``None``."""
        # NOR to slightly save the performance
        return not (self.mod or self.unit_affliction or self.unit_debuffs)


@dataclass
class DamagingHitData(HitData[ActionComponentHasHitLabels]):
    """
    Class for the data of a single raw damaging hit.

    Mods may be changed at this stage because some pre-conditions or bullet hits are not yet considered.
    For the actual single damaging hit, refer to :class:`DamageUnit`.
    """

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

    def to_affliction_unit(self, asset_action_condition: ActionConditionAsset) -> Optional[AppValueError]:
        """Get the affliction effect unit of this hit data. Returns ``None`` if not applicable."""
        return AbilityConditionConverter.to_affliction_unit(self, asset_action_condition)

    def to_debuff_units(self, asset_action_condition: ActionConditionAsset) -> list[ActionConditionEffectUnit]:
        """Get the debuff effect unit of this hit data. Returns an empty list if not applicable."""
        return AbilityConditionConverter.to_debuff_unit(self, asset_action_condition)

    def _damage_units_get_base(
            self, condition_comp: SkillConditionComposite, /,
            asset_action_condition: ActionConditionAsset, asset_action_info: PlayerActionInfoAsset
    ) -> list[DamageUnit]:
        hit_attr = self.hit_attr

        unit_affliction = self.to_affliction_unit(asset_action_condition)
        unit_debuff = self.to_debuff_units(asset_action_condition)

        # EXNOTE: Bullet timings like `msl` in dl-sim may be added here

        if self.will_deteriorate and condition_comp.bullet_hit_count:
            # Deteriorating bullets
            return [DamageUnit(self.damage_modifier_at_hit(hit_count), unit_affliction, unit_debuff, hit_attr.id)
                    for hit_count in range(1, condition_comp.bullet_hit_count_converted + 1)]

        if self.is_effective_inside_buff_zone:
            # Damage mods inside buff zones i.e. no damage mod if not in buff zone
            mods = self.mods_in_self_buff_zone(condition_comp.buff_zone_self_converted or 0)
            mods += self.mods_in_ally_buff_zone(condition_comp.buff_zone_ally_converted or 0)

            return [DamageUnit(mod, unit_affliction, unit_debuff, hit_attr.id) for mod in mods]

        if self.is_depends_on_user_buff_count:
            # Damage dealt depends on the user's buff count
            effective_buff_count = min(
                asset_action_info.get_data_by_id(self.action_id).max_bullet_count,
                condition_comp.buff_count_converted or 0
            )

            return [DamageUnit(hit_attr.damage_modifier, unit_affliction, unit_debuff, hit_attr.id)
                    for _ in range(effective_buff_count)]

        if self.is_depends_on_bullet_on_map:
            # Damage dealt depends on the bullets on the map
            return [DamageUnit(hit_attr.damage_modifier, unit_affliction, unit_debuff, hit_attr.id)
                    for _ in range(condition_comp.bullets_on_map_converted or 0)]

        if type(self.action_component) is ActionBullet:  # pylint: disable=unidiomatic-typecheck
            # Action component is exactly `ActionPartsBullet`, max hit count may be in effect
            # For example, Lin You S1 (`104503011`, AID `491040` and `491042`)
            return [DamageUnit(hit_attr.damage_modifier, unit_affliction, unit_debuff, hit_attr.id)
                    for _ in range(self.max_hit_count or 1)]

        # Cases not handled above
        return [DamageUnit(hit_attr.damage_modifier, unit_affliction, unit_debuff, hit_attr.id)]

    def _damage_units_apply_mod_boosts_target(
            self, damage_units: list[DamageUnit], condition_comp: SkillConditionComposite
    ):
        hit_attr = self.hit_attr

        # OD boosts
        if condition_comp.target_in_od:
            for damage_unit in damage_units:
                damage_unit.mod *= hit_attr.rate_boost_in_od

        # BK boosts
        if condition_comp.target_in_bk:
            for damage_unit in damage_units:
                damage_unit.mod *= hit_attr.rate_boost_in_bk

        # Punisher boosts
        if hit_attr.boost_on_target_afflicted and condition_comp.afflictions_converted & hit_attr.punisher_states:
            for damage_unit in damage_units:
                damage_unit.mod *= hit_attr.punisher_rate

    def _damage_units_apply_mod_boosts_self(
            self, damage_units: list[DamageUnit], condition_comp: SkillConditionComposite
    ):
        hit_attr = self.hit_attr

        # Crisis boosts
        if hit_attr.boost_by_hp:
            for damage_unit in damage_units:
                damage_unit.mod = calculate_crisis_mod(
                    damage_unit.mod, condition_comp.hp_status_converted, hit_attr.rate_boost_on_crisis
                )

        # Buff boosts
        if hit_attr.boost_by_buff_count and condition_comp.buff_count:
            for damage_unit in damage_units:
                damage_unit.mod *= (1 + hit_attr.rate_boost_by_buff * condition_comp.buff_count_converted)

    def _damage_units_apply_mod_boosts(self, damage_units: list[DamageUnit], condition_comp: SkillConditionComposite):
        self._damage_units_apply_mod_boosts_target(damage_units, condition_comp)
        self._damage_units_apply_mod_boosts_self(damage_units, condition_comp)

    def to_damage_units(
            self, condition_comp: SkillConditionComposite, /,
            asset_action_condition: ActionConditionAsset, asset_action_info: PlayerActionInfoAsset
    ) -> list[DamageUnit]:
        """
        Calculates the damage modifier of ``hit_data`` under ``condition_comp``.

        Usually, a single hit will have a single modifier.
        However, under some special circumstances (for example, deteriorating bullets),
        having multiple damage modifiers is possible.

        ``asset_action_info`` will be used for special circumstance mods calculation.
        If they are not provided, the mods may be uncalculatable or inaccurate.
        If such happens, an error will be raised, or a warning will be emitted.
        """
        # Early terminations / checks

        if self.pre_condition:
            # Pre-condition available, perform checks

            if self.pre_condition in SkillConditionCategories.skill_addl_inputs:
                # Pre-condition is additional inputs, perform special check
                pre_cond_addl_hit = SkillConditionCategories.skill_addl_inputs.convert(self.pre_condition)
                if pre_cond_addl_hit > (condition_comp.addl_inputs_converted or 0):
                    # Required pre-conditional additional inputs > additional inputs count in the condition,
                    # hit invalid
                    return []
            elif self.pre_condition not in condition_comp:
                # Other pre-conditions & not listed in the given condition composite i.e. pre-condition mismatch
                return []

        # Get base units

        damage_units = self._damage_units_get_base(condition_comp, asset_action_condition=asset_action_condition,
                                                   asset_action_info=asset_action_info)

        # Apply boosts

        self._damage_units_apply_mod_boosts(damage_units, condition_comp)

        # Return non-empty units only
        return [damage_unit for damage_unit in damage_units if not damage_unit.is_empty]
