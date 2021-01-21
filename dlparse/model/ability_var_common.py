"""
Common implementations for handling the ability variants across different types of the ability.

Types of the ability include but not limited to:

- Ability
- EX Ability
"""
from dataclasses import dataclass, field
from typing import Callable, Optional, TYPE_CHECKING, TypeVar

from dlparse.enums import (
    AbilityTargetAction, AbilityUpParameter, AbilityVariantType, BuffParameter, Condition, ConditionComposite,
    HitTargetSimple, Status,
)
from dlparse.errors import AbilityVariantUnconvertibleError
from dlparse.mono.asset import AbilityVariantEntry, ActionConditionEntry, ExAbilityEntry
from dlparse.mono.asset.base import AbilityEntryBase, AbilityVariantEntryBase
from .action_cond_conv import ActionCondEffectConvertPayload, ActionCondEffectConvertible
from .base import EffectUnitBase

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityVariantEffectUnit", "AbilityVariantEffectPayload", "ability_to_effect_units")


@dataclass(eq=False)
class AbilityVariantEffectUnit(EffectUnitBase):
    """The smallest unit of an ability effect coming from an ability variant."""

    source_ability_id: int
    condition_comp: ConditionComposite
    cooldown_sec: float
    max_occurrences: int

    rate_max: float

    target_action: AbilityTargetAction

    def __hash__(self):
        # x 1E5 for handling floating errors
        return hash((self.source_ability_id, self.condition_comp, self.parameter, int(self.rate * 1E5)))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return ((self.source_ability_id, self.condition_comp, int(self.parameter.value), self.rate)
                < (other.source_ability_id, other.condition_comp, int(other.parameter.value), other.rate))


A = TypeVar("A", bound=AbilityEntryBase)  # pylint: disable=invalid-name


@dataclass
class AbilityVariantEffectPayload(ActionCondEffectConvertPayload):
    """Payload object for variant effect conversion."""

    condition_comp: ConditionComposite
    condition_cooldown: float
    source_ability: A
    max_occurrences: int

    target_action: AbilityTargetAction = AbilityTargetAction.NONE

    source_ability_id: int = field(init=False)

    def __post_init__(self):
        self.source_ability_id = self.source_ability.id

    @property
    def is_source_ex_ability(self) -> bool:
        """Check if the source ability of this payload is an ex ability."""
        return isinstance(self.source_ability, ExAbilityEntry)


@dataclass
class AbilityVariantData(ActionCondEffectConvertible[AbilityVariantEffectUnit, AbilityVariantEffectPayload]):
    """An ability variant data class."""

    variant: AbilityVariantEntryBase

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
            cooldown_sec=payload.condition_cooldown,
            max_occurrences=payload.max_occurrences,
            source_ability_id=payload.source_ability_id,
            target_action=payload.target_action,
            status=Status.NONE,
            target=HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF,
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
            self, action_cond: "ActionConditionEntry", payload: AbilityVariantEffectPayload = None
    ) -> Optional[AbilityVariantEffectUnit]:
        return AbilityVariantEffectUnit(
            condition_comp=payload.condition_comp,
            cooldown_sec=payload.condition_cooldown,
            max_occurrences=payload.max_occurrences,
            source_ability_id=payload.source_ability_id,
            target_action=payload.target_action,
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

    def to_dispel_unit(
            self, param_enum: BuffParameter, action_cond: "ActionConditionEntry",
            payload: AbilityVariantEffectPayload = None
    ) -> Optional[AbilityVariantEffectUnit]:
        return AbilityVariantEffectUnit(
            condition_comp=payload.condition_comp,
            cooldown_sec=payload.condition_cooldown,
            max_occurrences=payload.max_occurrences,
            source_ability_id=payload.source_ability_id,
            target_action=payload.target_action,
            status=action_cond.afflict_status,
            target=HitTargetSimple.ENEMY,  # Buff dispel always target the enemy
            probability_pct=action_cond.probability_pct,
            rate=0,
            parameter=param_enum,
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

        max_value = 0
        if isinstance(self.variant, AbilityVariantEntry):
            max_value = asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id, on_not_found=0)

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                cooldown_sec=payload.condition_cooldown,
                max_occurrences=payload.max_occurrences,
                target_action=payload.target_action,
                parameter=ability_param.to_buff_parameter(payload.is_source_ex_ability),
                probability_pct=100,
                rate=self.variant.up_value / 100,  # Original data is percentage
                rate_max=max_value,
                target=HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            )
        }

    def _direct_effect_by_type(
            self, buff_param: BuffParameter, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        max_value = 0
        if isinstance(self.variant, AbilityVariantEntry):
            max_value = asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id, on_not_found=0)

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                cooldown_sec=payload.condition_cooldown,
                max_occurrences=payload.max_occurrences,
                target_action=payload.target_action,
                parameter=buff_param,
                probability_pct=100,  # Absolutely applicable
                rate=self.variant.up_value / 100,  # Original data is percentage
                rate_max=max_value,
                target=HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            )
        }

    def _from_skill_dmg_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_effect_by_type(BuffParameter.SKILL_DAMAGE, asset_manager, payload)

    def _from_crt_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_effect_by_type(BuffParameter.CRT_RATE, asset_manager, payload)

    def _from_rp_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_effect_by_type(BuffParameter.HEAL_RP, asset_manager, payload)

    def _from_od_gauge_dmg_up(self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload):
        return self._direct_effect_by_type(BuffParameter.OD_GAUGE_DAMAGE, asset_manager, payload)

    def _from_resist_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        resist_param = Status(self.variant.id_a).to_buff_param_resist()

        max_value = 0
        if isinstance(self.variant, AbilityVariantEntry):
            max_value = asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id, on_not_found=0)

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                cooldown_sec=payload.condition_cooldown,
                max_occurrences=payload.max_occurrences,
                target_action=payload.target_action,
                parameter=resist_param,
                probability_pct=100,  # Absolutely applicable
                rate=self.variant.up_value / 100,  # Original data is percentage
                rate_max=max_value,
                target=HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            )
        }

    def _from_change_state_dragons_claws(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        # Early terminate if the variant type is not ``AbilityVariantEntry``
        if not isinstance(self.variant, AbilityVariantEntry):
            return set()

        # As of 2020/01/20, all ``CHANGE_STATE`` ability variants that have all 3 ID slots set
        # is condition type 12 (``TRANSFORM_DRAGON``).
        # Therefore, we are not checking if the condition type matches and we overwrite the conditions in the payload.
        ret: set[AbilityVariantEffectUnit] = set()

        variant_ids = [
            var_id for var_id
            in (self.variant.id_a, self.variant.id_b, self.variant.id_c)
            if var_id  # Filter ineffective variant ID, because sometimes ID-C is not used
        ]
        conditions = [
            Condition.SELF_SHAPESHIFTED_1_TIME,
            Condition.SELF_SHAPESHIFTED_2_TIMES,
            Condition.SELF_SHAPESHIFTED_3_TIMES
        ]

        for action_cond_id, condition in zip(variant_ids, conditions):
            payload_new = AbilityVariantEffectPayload(
                condition_comp=ConditionComposite(condition),
                condition_cooldown=payload.condition_cooldown,
                source_ability=payload.source_ability,
                max_occurrences=payload.max_occurrences
            )

            ret.update(self.to_buff_units(
                asset_manager.asset_action_cond.get_data_by_id(action_cond_id), payload_new
            ))

        return ret

    def _from_change_state(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        # Add action condition IDs
        action_cond_ids: set[int] = set()

        # --- From action condition
        if payload.source_ability.condition.condition_type.is_shapeshifted_to_dragon:
            # --- Dragon's Claws
            return self._from_change_state_dragons_claws(asset_manager, payload)
        if action_cond_id := self.variant.assigned_action_condition:
            # Normal change state assignment
            action_cond_ids.add(action_cond_id)

        # --- From hit label
        if isinstance(self.variant, AbilityVariantEntry):
            if action_cond_id := self.variant.get_action_cond_id_hit_label(asset_manager):
                action_cond_ids.add(action_cond_id)

        # Get units from action condition IDs
        ret: set[AbilityVariantEffectUnit] = set()
        for action_cond_id in action_cond_ids:
            ret.update(self.to_buff_units(
                asset_manager.asset_action_cond.get_data_by_id(action_cond_id), payload
            ))
        return ret

    def _from_player_exp_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        max_value = 0
        if isinstance(self.variant, AbilityVariantEntry):
            max_value = asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id, on_not_found=0)

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                cooldown_sec=payload.condition_cooldown,
                max_occurrences=payload.max_occurrences,
                target_action=payload.target_action,
                parameter=BuffParameter.PLAYER_EXP,
                probability_pct=100,
                rate=self.variant.up_value / 100,  # Original data is percentage
                rate_max=max_value,
                target=HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            )
        }

    def _from_sp_charge(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        charge_params = {
            BuffParameter.SP_CHARGE_PCT_S1, BuffParameter.SP_CHARGE_PCT_S2,
            BuffParameter.SP_CHARGE_PCT_S3, BuffParameter.SP_CHARGE_PCT_S4
        }

        max_value = 0
        if isinstance(self.variant, AbilityVariantEntry):
            max_value = asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id, on_not_found=0)

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp,
                cooldown_sec=payload.condition_cooldown,
                max_occurrences=payload.max_occurrences,
                target_action=payload.target_action,
                parameter=param,
                probability_pct=100,
                rate=self.variant.up_value / 100,  # Original data is percentage
                rate_max=max_value,
                target=HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF,
                status=Status.NONE,
                duration_time=0,
                duration_count=0,
                max_stack_count=0,
                slip_damage_mod=0,
                slip_interval=0,
            ) for param in charge_params
        }

    def _from_action_grant(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        action_grant_data = asset_manager.asset_action_grant.get_data_by_id(self.variant.id_a)
        action_cond_data = asset_manager.asset_action_cond.get_data_by_id(action_grant_data.action_condition_id)

        payload.target_action = action_grant_data.target_action

        units: set[AbilityVariantEffectUnit] = set(self.to_buff_units(action_cond_data, payload))
        units.update(self.to_dispel_units(action_cond_data, payload))

        return units

    def to_effect_units(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        """
        Get the ability variant effect units of this ability variant.

        :raises AbilityVariantUnconvertibleError: if the variant type is not handled / unconvertible
        """
        if self.type_enum == AbilityVariantType.HIT_ATTR_SHIFT:
            return set()

        unit_method = Callable[["AssetManager", AbilityVariantEffectPayload], set[AbilityVariantEffectUnit]]
        method_dict: dict[AbilityVariantType, unit_method] = {
            AbilityVariantType.STATUS_UP: self._from_status_up,
            AbilityVariantType.SKILL_DMG_UP: self._from_skill_dmg_up,
            AbilityVariantType.CRT_RATE_UP: self._from_crt_up,
            AbilityVariantType.OD_GAUGE_DMG_UP: self._from_od_gauge_dmg_up,
            AbilityVariantType.RP_UP: self._from_rp_up,
            AbilityVariantType.RESISTANCE_UP: self._from_resist_up,
            AbilityVariantType.CHANGE_STATE: self._from_change_state,
            AbilityVariantType.PLAYER_EXP_UP: self._from_player_exp_up,
            AbilityVariantType.SP_CHARGE: self._from_sp_charge,
            AbilityVariantType.ACTION_GRANT: self._from_action_grant
        }

        for var_type, method in method_dict.items():
            if self.type_enum == var_type:
                return method(asset_manager, payload)

        raise AbilityVariantUnconvertibleError(payload.source_ability_id, self.variant.type_id)


T = TypeVar("T", bound=AbilityEntryBase)


def ability_to_effect_units(
        ability_entry: T, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
) -> set[AbilityVariantEffectUnit]:
    """Convert ``ability_entry`` to a set of variant effect units."""
    effect_units: set[AbilityVariantEffectUnit] = set()

    for variant in ability_entry.variants:
        if variant.type_enum == AbilityVariantType.OTHER_ABILITY:
            continue  # Refer to the other ability, no variant effect

        effect_units.update(AbilityVariantData(variant).to_effect_units(asset_manager, payload))

    return effect_units