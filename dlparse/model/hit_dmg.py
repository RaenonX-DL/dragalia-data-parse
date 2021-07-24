"""Class for a single damaging hit."""
from dataclasses import dataclass, field
from functools import cache
from itertools import product
from typing import Optional, TYPE_CHECKING

from dlparse.enums import Condition, ConditionComposite, FireStockPattern
from dlparse.errors import AppValueError, BulletEndOfLifeError, DamagingHitValidationFailedError
from dlparse.mono.asset import (
    ActionBuffField, ActionBullet, ActionBulletStockFire, ActionComponentHasHitLabels, ActionConditionAsset,
    BuffCountAsset, HitAttrEntry,
)
from dlparse.utils import calculate_crisis_mod
from .action_cond_effect import EnemyAfflictionEffectUnit, HitActionConditionEffectUnit
from .hit_conv import HitDataEffectConvertible

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("DamagingHitData", "DamageUnit")


@dataclass
class DamageUnit:
    """Class for a single actual damage hit."""

    hit_time: float

    mod: float
    unit_affliction: Optional[EnemyAfflictionEffectUnit]
    unit_debuffs: list[HitActionConditionEffectUnit]
    hit_attr: HitAttrEntry

    dispel: bool = False

    counter_mod: float = field(init=False)

    def __post_init__(self):
        if self.unit_affliction and not isinstance(self.unit_affliction, EnemyAfflictionEffectUnit):
            raise AppValueError(f"Unexpected affliction unit type {type(self.unit_affliction)}")

        self.counter_mod = self.hit_attr.damage_modifier_counter

    @property
    def is_empty(self) -> bool:
        """Check if the damage unit is empty. Empty here means that the mod is ``0`` and both units are ``None``."""
        # NOR to slightly save the performance
        return not (self.mod or self.unit_affliction or self.unit_debuffs or self.dispel)


@dataclass
class DamagingHitData(HitDataEffectConvertible[ActionComponentHasHitLabels]):
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

    # region Damage modifiers when inside the buff fields
    mod_on_self_buff_field: float = 0
    mod_on_ally_buff_field: float = 0
    # endregion

    # region Flags of bullets having special patterns
    is_depends_on_bullet_summoned: bool = False
    is_depends_on_user_buff_count: bool = False
    is_depends_on_bullet_on_map: bool = False
    # endregion

    # region Other attributes
    is_boost_by_gauge_filled: bool = False

    boost_by_combo_conditions_ability: set[Condition] = field(default_factory=set)

    # endregion

    def __hash__(self):
        # Enable the use of `@cache`
        return id(self)

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

                # Only stores the max hit count if:
                # - depends on count of bullets summoned
                # - max count embedded in the action component
                if (
                        self.action_component.is_depends_on_bullet_summoned
                        or self.action_component.pattern == FireStockPattern.USER_BUFF_COUNT_DEPENDENT_EMBEDDED
                ):
                    self.max_hit_count = self.action_component.max_hit_count

            # Set the max hit count except for stock bullets in special stocking pattern
            if not (
                    isinstance(self.action_component, ActionBulletStockFire)
                    and self.action_component.is_special_pattern
            ):
                self.max_hit_count = self.action_component.max_hit_count

        # Buff field specific damage mod
        if isinstance(self.action_component, ActionBuffField):
            if self.action_component.count_for_self_built:
                self.mod_on_self_buff_field = self.hit_attr.damage_modifier
            else:
                self.mod_on_ally_buff_field = self.hit_attr.damage_modifier

        # Other attributes from ability data
        if self.ability_data:
            for ability_data in self.ability_data:
                self.boost_by_combo_conditions_ability.update(ability_data.boost_by_combo_conditions)

            self.is_boost_by_gauge_filled = any(
                ability_data.is_boost_by_gauge_status for ability_data in self.ability_data
            )

        self._init_validity_check()

    @property
    def is_effective_inside_buff_field(self) -> bool:
        """Check if the hit is only effective if the user is inside buff fields."""
        return bool(self.mod_on_self_buff_field or self.mod_on_ally_buff_field)

    def get_hit_count(
            self, original_hit_count: int, condition_comp: ConditionComposite, asset_manager: "AssetManager"
    ) -> int:
        damage_units = self.to_damage_units(condition_comp, original_hit_count, asset_manager=asset_manager)

        count = len([unit for unit in damage_units if unit.mod])
        count += (self.hit_attr.dummy_hit_count * ((condition_comp.teammate_coverage_converted or 0) + 1))

        return count

    def damage_modifier_at_hit(self, hit_count: int) -> float:
        """
        Get the damage modifier at hit ``hit_count``.

        If the damage hit will not deteriorate, return the original damage modifier.

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

    def mods_in_self_buff_field(self, count: int) -> list[float]:
        """Get the damage modifiers if standing on ``count`` buff fields created by the user."""
        return [self.mod_on_self_buff_field] * count

    def mods_in_ally_buff_field(self, count: int) -> list[float]:
        """Get the damage modifiers if standing on ``count`` buff fields created by the allies."""
        return [self.mod_on_ally_buff_field] * count

    def _damage_units_get_base_attributes(
            self, condition_comp: ConditionComposite, unit_affliction: EnemyAfflictionEffectUnit,
            units_debuff: list[HitActionConditionEffectUnit], /,
            asset_manager: "AssetManager"
    ) -> Optional[list[DamageUnit]]:
        """
        Get the base damage units according to the hit data attributes.

        Return ``None`` if the hit data attributes cannot determine the base damage units yet.
        """
        hit_attr = self.hit_attr

        if self.will_deteriorate and condition_comp.bullet_hit_count:
            # Deteriorating bullets
            return [
                DamageUnit(
                    self.action_time, self.damage_modifier_at_hit(hit_count), unit_affliction, units_debuff, hit_attr
                )
                for hit_count in range(1, condition_comp.bullet_hit_count_converted + 1)
            ]

        if self.is_effective_inside_buff_field:
            # Damage mods inside buff fields i.e. no damage mod if not in buff field
            mods = self.mods_in_self_buff_field(condition_comp.buff_field_self_converted or 0)
            mods += self.mods_in_ally_buff_field(condition_comp.buff_field_ally_converted or 0)

            return [DamageUnit(self.action_time, mod, unit_affliction, units_debuff, hit_attr) for mod in mods]

        if self.is_depends_on_bullet_summoned or self.is_depends_on_bullet_on_map:
            # Damage dealt depends on the bullets summoned / bullets on the map
            return [
                DamageUnit(self.action_time, hit_attr.damage_modifier, unit_affliction, units_debuff, hit_attr)
                for _ in range(condition_comp.bullets_on_map_converted or 0)
            ]

        if self.is_depends_on_user_buff_count:
            action_info = asset_manager.asset_action_info_player.get_data_by_id(self.action_id)

            # Damage dealt depends on the user's buff count
            effective_buff_count = min(
                action_info.max_bullet_count or self.max_hit_count,
                condition_comp.buff_count_converted or 0
            )
            return [
                DamageUnit(self.action_time, hit_attr.damage_modifier, unit_affliction, units_debuff, hit_attr)
                for _ in range(effective_buff_count)
            ]

        return None

    def _damage_units_get_base(
            self, condition_comp: ConditionComposite, hit_count: int, /, asset_manager: "AssetManager"
    ) -> list[DamageUnit]:
        hit_attr = self.hit_attr

        # Get affliction unit & buff dispel
        unit_affliction = None
        dispel = False
        if action_cond_id := self.action_condition_id:
            action_cond = asset_manager.asset_action_cond.get_data_by_id(action_cond_id)

            dispel = action_cond.is_dispel_buff
            unit_affliction = self.to_affliction_unit(action_cond)

        units_debuff = self.to_debuff_units(asset_manager.asset_action_cond)

        # EXNOTE: Bullet timings like `msl` in dl-sim may be added here

        # This must be before the check of `type(self.action_component) is ActionBullet`
        # because the hit attribute will be ineffective if the hit count does not match the hit condition,
        # which implies that the type of the action component is meaningless
        if not hit_attr.is_effective_hit_count(hit_count):
            # Hit attribute is not effective when the user's hit count is ``hit_count``
            return []

        base_units_by_attr = self._damage_units_get_base_attributes(
            condition_comp, unit_affliction, units_debuff, asset_manager=asset_manager
        )
        # Explicitly checking `None` because both `None` and empty list is falsy while
        # `None` means no early termination condition met; an empty list means no damage unit
        if base_units_by_attr is not None:
            # Class attributes can determine the base damage units, return it
            return base_units_by_attr

        damage_units = [DamageUnit(
            self.action_time, hit_attr.damage_modifier, unit_affliction, units_debuff, hit_attr, dispel=dispel
        )]

        if type(self.action_component) is ActionBullet:  # pylint: disable=unidiomatic-typecheck
            # Action component is exactly `ActionPartsBullet`, max hit count may be in effect
            # For example, Lin You S1 (`104503011`, AID `491040` and `491042`)
            return damage_units * (self.max_hit_count or 1)

        # Cases not handled above
        return damage_units

    def _damage_units_apply_mod_boosts_target(
            self, damage_units: list[DamageUnit], condition_comp: ConditionComposite
    ):
        hit_attr = self.hit_attr

        # OD boosts
        if condition_comp.target_in_od:
            for damage_unit in damage_units:
                damage_unit.mod *= hit_attr.rate_boost_od

        # Punisher boosts
        if (
                hit_attr.boost_on_target_afflicted
                and condition_comp.target_afflictions_converted & hit_attr.punisher_states
        ):
            for damage_unit in damage_units:
                damage_unit.mod *= hit_attr.get_combo_punisher_rate(condition_comp.combo_count_converted)

    def _damage_units_apply_mod_boosts_self(
            self, damage_units: list[DamageUnit], condition_comp: ConditionComposite, /,
            asset_buff_count: BuffCountAsset
    ):
        hit_attr = self.hit_attr

        # Crisis boosts
        if hit_attr.boost_by_hp:
            for damage_unit in damage_units:
                damage_unit.mod = calculate_crisis_mod(
                    damage_unit.mod, condition_comp.hp_status_converted, hit_attr.rate_boost_on_crisis
                )

        # Buff boosts
        if hit_attr.boost_by_buff_count and condition_comp.has_buff_boost_condition:
            damage_boost_rate = condition_comp.get_boost_rate_by_buff(hit_attr, asset_buff_count)

            for damage_unit in damage_units:
                damage_unit.mod *= (1 + damage_boost_rate)

        # Combo damage boosts
        if condition_comp.combo_count_converted and self.boost_by_combo_conditions_ability:
            for ability_data, damage_unit in product(self.ability_data, damage_units):
                damage_unit.mod *= (1 + ability_data.get_boost_by_combo(condition_comp.combo_count_converted))

        # Gauge fill boosts
        if condition_comp.gauge_filled_converted and self.is_boost_by_gauge_filled:
            for ability_data, damage_unit in product(self.ability_data, damage_units):
                boost_rate = 1 + ability_data.get_boost_by_gauge_filled_dmg(condition_comp.gauge_filled_converted)
                damage_unit.mod *= boost_rate

    def _damage_units_apply_mod_boosts(
            self, damage_units: list[DamageUnit], condition_comp: ConditionComposite, /,
            asset_buff_count: BuffCountAsset
    ):
        self._damage_units_apply_mod_boosts_target(damage_units, condition_comp)
        self._damage_units_apply_mod_boosts_self(damage_units, condition_comp, asset_buff_count=asset_buff_count)

    def _damage_units_from_action_cond(self, asset_action_condition: ActionConditionAsset):
        # Get affliction unit & dispel
        unit_affliction = None
        dispel = False
        if action_cond_id := self.action_condition_id:
            action_cond = asset_action_condition.get_data_by_id(action_cond_id)

            dispel = action_cond.is_dispel_buff
            unit_affliction = self.to_affliction_unit(action_cond)

        # Get the damage unit that marks the enemy
        return [DamageUnit(
            self.action_time,
            0,
            unit_affliction,
            self.to_debuff_units(asset_action_condition),
            self.hit_attr,
            dispel=dispel
        )]

    def _check_early_return_pre_cond(
            self, condition_comp: ConditionComposite, asset_action_condition: ActionConditionAsset
    ) -> Optional[list[DamageUnit]]:
        # Pre-condition available, perform checks
        if pre_cond_addl_hit := self.pre_condition_comp.addl_inputs_converted:
            # Pre-condition is additional inputs, perform special check
            if pre_cond_addl_hit != (condition_comp.addl_inputs_converted or 0):
                # Requires pre-conditional additional inputs = additional inputs count in the condition
                return []
        elif self.pre_condition_comp.mark_explode and not condition_comp.mark_explode:
            return self._damage_units_from_action_cond(asset_action_condition)
        elif self.pre_condition_comp not in condition_comp:
            # Other pre-conditions & not fully listed in the given condition composite i.e. pre-condition mismatch
            return []

        return None

    def _check_early_return(
            self, condition_comp: ConditionComposite, asset_action_condition: ActionConditionAsset
    ) -> Optional[list[DamageUnit]]:
        # Has precondition
        if self.pre_condition_comp:
            damage_units_pre_cond = self._check_early_return_pre_cond(condition_comp, asset_action_condition)
            # Explicit check to distinguish "not to early return" and "return an empty array"
            if damage_units_pre_cond is not None:
                return damage_units_pre_cond

        # Action cancel
        if condition_comp.action_cancel and not self.pre_condition_comp.action_cancel:
            # If action canceling is included in the conditions,
            # only the actions to be executed after the cancel should be returned.
            # -------------------------------------------------------------------
            # For example, `991061` is executed only if Formal Joachim S1 (109503011) is used
            # to cancel his S2 `991070` (and `991060` will not be executed / will be interrupted).
            # If no cancellation is used, `991060` will be executed completely and no execution of `991061` instead.
            return []

        # Counter action
        if condition_comp.action_counter_red and not self.pre_condition_comp.action_counter_red:
            # If counter action is included in the conditions,
            # only the actions to be executed after countering should be returned.
            # -------------------------------------------------------------------
            # For example, `991101` is executed only if Yoshitsune S1 (109502021)
            # successfully countered an red attack during `991100`.
            # If the counter is failed, `991100` should be fully executed, and `991101` will not execute.
            return []

        # Mark explosion
        if condition_comp.mark_explode and not self.pre_condition_comp.mark_explode:
            # Mark explosion damage is requested, but the damaging hit is not the explosion damage
            return []

        return None

    # Cache the function because it is used for getting the hit count
    # and for getting the actual damage units.
    # These two calls could appear in different places.
    @cache
    def to_damage_units(
            self, condition_comp: ConditionComposite, hit_count: int, /, asset_manager: "AssetManager"
    ) -> list[DamageUnit]:
        """
        Calculates the damage modifier under ``condition_comp`` when the skill has dealt ``hit_count`` hits.

        Usually, a single hit will have a single modifier.
        However, under some special circumstances (for example, deteriorating bullets),
        having multiple damage modifiers is possible.
        """
        # --- Early return check

        damage_units = self._check_early_return(condition_comp, asset_manager.asset_action_cond)
        # Explicit check to distinguish "not to early return" and "return an empty array"
        if damage_units is not None:
            return damage_units

        # --- Calculate mods

        # Get base units
        damage_units = self._damage_units_get_base(condition_comp, hit_count, asset_manager=asset_manager)

        # Apply boosts
        self._damage_units_apply_mod_boosts(
            damage_units, condition_comp, asset_buff_count=asset_manager.asset_buff_count
        )

        # Return non-empty units only
        return [damage_unit for damage_unit in damage_units if not damage_unit.is_empty]
