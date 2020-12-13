"""Class for a single damaging hit."""
from dataclasses import dataclass
from itertools import product
from typing import Optional

from dlparse.enums import SkillCondition, SkillConditionCategories, SkillConditionComposite
from dlparse.errors import AppValueError, BulletEndOfLifeError, DamagingHitValidationFailedError
from dlparse.mono.asset import (
    ActionBuffField, ActionBullet, ActionBulletStockFire, ActionComponentHasHitLabels, ActionConditionAsset,
    PlayerActionInfoAsset,
)
from dlparse.utils import calculate_crisis_mod
from .effect_action_cond import ActionConditionEffectUnit, AfflictionEffectUnit
from .hit_unit import UnitsConvertibleHitData

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
class DamagingHitData(UnitsConvertibleHitData[ActionComponentHasHitLabels]):
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
    is_depends_on_bullet_summoned: bool = False
    is_depends_on_user_buff_count: bool = False
    is_depends_on_bullet_on_map: bool = False
    # endregion

    # region Other attributes
    is_boost_by_combo: bool = False
    is_boost_by_gauge_filled: bool = False

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
                self.is_depends_on_bullet_summoned = self.action_component.is_depends_on_bullet_summoned
                self.is_depends_on_user_buff_count = self.action_component.is_depends_on_user_buff_count
                self.is_depends_on_bullet_on_map = self.action_component.is_depends_on_bullet_on_map

                # Only stores the max hit count if depends on count of bullets summoned
                if self.action_component.is_depends_on_bullet_summoned:
                    self.max_hit_count = self.action_component.max_hit_count

            # Set the max hit count except for stock bullets in special stocking pattern
            if not (isinstance(self.action_component, ActionBulletStockFire)
                    and self.action_component.is_special_pattern):
                self.max_hit_count = self.action_component.max_hit_count

        # Buff zone specific damage mod
        if isinstance(self.action_component, ActionBuffField):
            if self.action_component.count_for_self_built:
                self.mod_on_self_buff_zone = self.hit_attr.damage_modifier
            else:
                self.mod_on_ally_buff_zone = self.hit_attr.damage_modifier

        # Other attributes
        if self.ability_data:
            self.is_boost_by_combo = any(
                ability_data.is_boost_by_combo for ability_data in self.ability_data
            )
            self.is_boost_by_gauge_filled = any(
                ability_data.is_boost_by_gauge_status for ability_data in self.ability_data
            )

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

    def _damage_units_get_base_attributes(
            self, condition_comp: SkillConditionComposite, unit_affliction: AfflictionEffectUnit,
            units_debuff: list[ActionConditionEffectUnit], /,
            asset_action_info: PlayerActionInfoAsset
    ) -> Optional[list[DamageUnit]]:
        """
        Get the base damage units according to the hit data attributes.

        Returns ``None`` if the hit data attributes cannot determine the base damage units yet.
        """
        hit_attr = self.hit_attr

        if self.will_deteriorate and condition_comp.bullet_hit_count:
            # Deteriorating bullets
            return [
                DamageUnit(self.damage_modifier_at_hit(hit_count), unit_affliction, units_debuff, hit_attr.id)
                for hit_count in range(1, condition_comp.bullet_hit_count_converted + 1)
            ]

        if self.is_effective_inside_buff_zone:
            # Damage mods inside buff zones i.e. no damage mod if not in buff zone
            mods = self.mods_in_self_buff_zone(condition_comp.buff_zone_self_converted or 0)
            mods += self.mods_in_ally_buff_zone(condition_comp.buff_zone_ally_converted or 0)

            return [DamageUnit(mod, unit_affliction, units_debuff, hit_attr.id) for mod in mods]

        if self.is_depends_on_bullet_summoned or self.is_depends_on_bullet_on_map:
            # Damage dealt depends on the bullets summoned / bullets on the map
            return [
                DamageUnit(hit_attr.damage_modifier, unit_affliction, units_debuff, hit_attr.id)
                for _ in range(condition_comp.bullets_on_map_converted or 0)
            ]

        if self.is_depends_on_user_buff_count:
            # Damage dealt depends on the user's buff count
            effective_buff_count = min(
                asset_action_info.get_data_by_id(self.action_id).max_bullet_count,
                condition_comp.buff_count_converted or 0
            )
            return [
                DamageUnit(hit_attr.damage_modifier, unit_affliction, units_debuff, hit_attr.id)
                for _ in range(effective_buff_count)
            ]

        return None

    def _damage_units_get_base(
            self, condition_comp: SkillConditionComposite, hit_count: int, /,
            asset_action_condition: ActionConditionAsset, asset_action_info: PlayerActionInfoAsset
    ) -> list[DamageUnit]:
        hit_attr = self.hit_attr

        unit_affliction = self.to_affliction_unit(asset_action_condition)
        units_debuff = self.to_debuff_units(asset_action_condition)

        # EXNOTE: Bullet timings like `msl` in dl-sim may be added here

        # This must be before the check of `type(self.action_component) is ActionBullet`
        # because the hit attribute will be ineffective if the hit count does not match the hit condition,
        # which implies that the type of the action component is meaningless
        if not hit_attr.is_effective_hit_count(hit_count):
            # Hit attribute is not effective when the user's hit count is ``hit_count``
            return []

        base_units_by_attr = self._damage_units_get_base_attributes(
            condition_comp, unit_affliction, units_debuff, asset_action_info=asset_action_info
        )
        # Explicitly checking `None` because both `None` and empty list is falsy while
        # `None` means no early termination condition met; an empty list means no damage unit
        if base_units_by_attr is not None:
            # Class attributes can determine the base damage units, return it
            return base_units_by_attr

        if type(self.action_component) is ActionBullet:  # pylint: disable=unidiomatic-typecheck
            # Action component is exactly `ActionPartsBullet`, max hit count may be in effect
            # For example, Lin You S1 (`104503011`, AID `491040` and `491042`)
            return [
                DamageUnit(hit_attr.damage_modifier, unit_affliction, units_debuff, hit_attr.id)
                for _ in range(self.max_hit_count or 1)
            ]

        # Cases not handled above
        return [DamageUnit(hit_attr.damage_modifier, unit_affliction, units_debuff, hit_attr.id)]

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

        # Combo damage boosts
        if condition_comp.combo_count_converted and self.is_boost_by_combo:
            for ability_data, damage_unit in product(self.ability_data, damage_units):
                damage_unit.mod *= (1 + ability_data.get_boost_by_combo(condition_comp.combo_count_converted))

        # Combo damage boosts
        if condition_comp.gauge_filled_converted and self.is_boost_by_gauge_filled:
            for ability_data, damage_unit in product(self.ability_data, damage_units):
                boost_rate = 1 + ability_data.get_boost_by_gauge_filled_dmg(condition_comp.gauge_filled_converted)
                damage_unit.mod *= boost_rate

    def _damage_units_apply_mod_boosts(self, damage_units: list[DamageUnit], condition_comp: SkillConditionComposite):
        self._damage_units_apply_mod_boosts_target(damage_units, condition_comp)
        self._damage_units_apply_mod_boosts_self(damage_units, condition_comp)

    def to_damage_units(
            self, condition_comp: SkillConditionComposite, hit_count: int, /,
            asset_action_condition: ActionConditionAsset, asset_action_info: PlayerActionInfoAsset
    ) -> list[DamageUnit]:
        """
        Calculates the damage modifier under ``condition_comp`` when the skill has dealt ``hit_count`` hits.

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
            elif self.pre_condition == SkillCondition.MARK_EXPLODES and not condition_comp.mark_explode:
                # Pre-condition is marking: if condition to explode the mark, returns the damage (pass this check).
                # Otherwise, returns the marking debuff unit.
                return [DamageUnit(
                    0,
                    self.to_affliction_unit(asset_action_condition),
                    self.to_debuff_units(asset_action_condition),
                    self.hit_attr.id
                )]
            elif self.pre_condition not in condition_comp:
                # Other pre-conditions & not listed in the given condition composite i.e. pre-condition mismatch
                return []

        if condition_comp.action_cancel and self.pre_condition != condition_comp.action_cancel:
            # If action canceling is included in the conditions,
            # only the actions to be executed after the cancel should be returned
            # -------------------------------------------------------------------
            # For example, `991061` is executed only if Formal Joachim S1 (109503011) is used
            # to cancel his S2 `991070` (and `991060` will not be executed / will be interrupted).
            # If no cancellation is used, `991060` will be executed completely and no execution of `991061` instead.
            return []

        if condition_comp.mark_explode and self.pre_condition != SkillCondition.MARK_EXPLODES:
            # Condition wants the mark explode damage, but the damage hit is not the explosion damage
            return []

        # Get base units

        damage_units = self._damage_units_get_base(
            condition_comp, hit_count,
            asset_action_condition=asset_action_condition, asset_action_info=asset_action_info
        )

        # Apply boosts

        self._damage_units_apply_mod_boosts(damage_units, condition_comp)

        # Return non-empty units only
        return [damage_unit for damage_unit in damage_units if not damage_unit.is_empty]
