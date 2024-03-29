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
    Element, HitTargetSimple, Status,
)
from dlparse.errors import AbilityVariantUnconvertibleError
from dlparse.mono.asset import AbilityVariantEntry, ActionConditionEntry, ExAbilityEntry
from dlparse.mono.asset.extension import AbilityEntryExtension
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
        return hash((self.source_ability_id, self.condition_comp, self.parameter, int(round(self.rate * 1E5))))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return ((self.source_ability_id, self.condition_comp, int(self.parameter.value), self.rate)
                < (other.source_ability_id, other.condition_comp, int(other.parameter.value), other.rate))


AT = TypeVar("AT", bound=AbilityEntryExtension)


@dataclass
class AbilityVariantEffectPayload(ActionCondEffectConvertPayload):
    """Payload object for variant effect conversion."""

    condition_comp: ConditionComposite
    condition_cooldown: float
    source_ability: AT
    max_occurrences: int

    target_action: AbilityTargetAction = AbilityTargetAction.NONE

    is_chained_ex: bool = False

    source_ability_id: int = field(init=False)
    condition_probability: float = field(init=False)
    max_stack_count: int = field(init=False)

    def __post_init__(self):
        self.source_ability_id = self.source_ability.id
        self.condition_probability = self.source_ability.condition.probability
        self.max_stack_count = self.source_ability.condition.max_stack_count

    @property
    def is_source_ex_ability(self) -> bool:
        """Check if the source ability of this payload is either an EX or a chained EX ability."""
        return self.is_chained_ex or self.is_source_strict_ex_ability

    @property
    def is_source_strict_ex_ability(self) -> bool:
        """
        Check if the source ability of this payload is an EX ability.

        Note that this will return ``False`` if the source ability is chained EX, not actually EX.
        """
        return isinstance(self.source_ability, ExAbilityEntry)


@dataclass
class AbilityVariantData(ActionCondEffectConvertible[AbilityVariantEffectUnit, AbilityVariantEffectPayload]):
    """An ability variant data class."""

    variant: AbilityVariantEntry

    type_enum: AbilityVariantType = field(init=False)

    def __post_init__(self):
        self.type_enum = AbilityVariantType(self.variant.type_id)

    def to_param_up(
            self, param_enum: BuffParameter, param_rate: float, action_cond: ActionConditionEntry,
            payload: AbilityVariantEffectPayload = None
    ) -> Optional[AbilityVariantEffectUnit]:
        if not param_rate:
            return None  # Rate is 0, parameter not raised

        return self._action_cond_unit(param_enum, param_rate, action_cond, payload)

    def to_affliction_unit(
            self, action_cond: "ActionConditionEntry", payload: AbilityVariantEffectPayload = None
    ) -> Optional[AbilityVariantEffectUnit]:
        return self.to_param_up(BuffParameter.AFFLICTION, 0, action_cond, payload)

    def to_dispel_unit(
            self, param_enum: BuffParameter, action_cond: "ActionConditionEntry",
            payload: AbilityVariantEffectPayload = None
    ) -> Optional[AbilityVariantEffectUnit]:
        return self._action_cond_unit(param_enum, 0, action_cond, payload, target=HitTargetSimple.ENEMY)

    @staticmethod
    def _action_cond_unit(
            param_enum: BuffParameter, param_rate: float, action_cond: ActionConditionEntry,
            payload: AbilityVariantEffectPayload = None, /,
            target: Optional[HitTargetSimple] = None
    ) -> AbilityVariantEffectUnit:
        if not target:
            target = HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF

        max_stack_count = action_cond.max_stack_count
        if param_enum.is_duration_count_meaningless:
            max_stack_count = 0

        return AbilityVariantEffectUnit(
            condition_comp=payload.condition_comp,
            cooldown_sec=payload.condition_cooldown,
            max_occurrences=payload.max_occurrences,
            source_ability_id=payload.source_ability_id,
            target_action=payload.target_action,
            status=action_cond.afflict_status,
            target=target,
            parameter=param_enum,
            probability_pct=payload.condition_probability or action_cond.probability_pct,
            rate=param_rate,
            rate_max=0,
            max_stack_count=max_stack_count,
            duration_sec=action_cond.duration_sec,
            duration_count=0 if param_enum.is_duration_count_meaningless else action_cond.duration_count,
            slip_interval_sec=action_cond.slip_interval_sec,
            slip_damage_mod=action_cond.slip_damage_mod,
        )

    def _direct_buff_unit(
            self, buff_param: BuffParameter, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload, /,
            addl_cond_comp: Optional[ConditionComposite] = None, val_div_100: bool = True
    ) -> set[AbilityVariantEffectUnit]:
        max_value = 0
        if isinstance(self.variant, AbilityVariantEntry):
            max_value = asset_manager.asset_ability_limit.get_max_value(self.variant.limited_group_id, on_not_found=0)

        up_value = self.variant.up_value
        if val_div_100:
            up_value /= 100

        return {
            AbilityVariantEffectUnit(
                source_ability_id=payload.source_ability_id,
                condition_comp=payload.condition_comp + addl_cond_comp,
                cooldown_sec=payload.condition_cooldown,
                max_occurrences=payload.max_occurrences,
                target_action=payload.target_action,
                parameter=buff_param,
                probability_pct=payload.condition_probability or 100,  # Some conditions may have probabilty assigned
                rate=up_value,
                rate_max=max_value,
                target=HitTargetSimple.TEAM if payload.is_source_ex_ability else HitTargetSimple.SELF,
                status=Status.NONE,
                duration_sec=0,
                duration_count=0,
                max_stack_count=payload.source_ability.condition.max_stack_count,
                slip_damage_mod=0,
                slip_interval_sec=0,
            )
        }

    def _from_status_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        ability_param = AbilityUpParameter(self.variant.id_a)

        if ability_param == AbilityUpParameter.NONE:
            # Ability up is dummy (no effect), return an empty set
            # > This happens on Gala Leonidas AB1@Lv1 (1460), where the description only says
            # > "Leonidas only shapeshift to Mars." In this case, this serves as a dummy ability variant.
            return set()

        return self._direct_buff_unit(
            ability_param.to_buff_parameter(payload.is_source_strict_ex_ability), asset_manager, payload
        )

    def _from_dmg_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        buff_param = None

        # Set the buff param
        if self.variant.target_action_enum == AbilityTargetAction.AUTO:
            buff_param = BuffParameter.AUTO_DAMAGE
        elif self.variant.target_action_enum == AbilityTargetAction.FORCE_STRIKE:
            buff_param = BuffParameter.FS_DAMAGE_PASSIVE
        elif self.variant.target_action_enum == AbilityTargetAction.SKILL_ALL:
            buff_param = BuffParameter.SKILL_DAMAGE_PASSIVE
        elif self.variant.target_action_enum == AbilityTargetAction.NONE:
            if Condition.TARGET_ATK_OR_DEF_DOWN in payload.condition_comp:
                buff_param = BuffParameter.ATK_OR_DEF_DOWN_PUNISHER
            if Condition.TARGET_OD_STATE in payload.condition_comp:
                buff_param = BuffParameter.OD_STATE_PUNISHER

        if not buff_param:
            # Raise error if buff param not defined (behavior not defined)
            raise AbilityVariantUnconvertibleError(
                payload.source_ability_id, self.variant.type_id, f"Target action: {self.variant.target_action_enum}"
            )

        return self._direct_buff_unit(buff_param, asset_manager, payload)

    def _from_crt_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.CRT_RATE_PASSIVE, asset_manager, payload)

    def _from_crt_dmg_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.CRT_DAMAGE_PASSIVE, asset_manager, payload)

    def _from_elem_dmg_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(Element(self.variant.id_a).to_elem_dmg_up(), asset_manager, payload)

    def _from_elem_resist_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(Element(self.variant.id_a).to_elem_res_up_passive(), asset_manager, payload)

    def _from_rp_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.RP_UP, asset_manager, payload)

    def _from_dragon_dmg_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.DRAGON_DAMAGE, asset_manager, payload)

    def _from_od_gauge_dmg_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.OD_GAUGE_DAMAGE, asset_manager, payload)

    def _from_buff_time_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.TARGETED_BUFF_TIME, asset_manager, payload)

    def _from_resist_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        resist_param = Status(self.variant.id_a).to_buff_param_resist()

        return self._direct_buff_unit(resist_param, asset_manager, payload)

    def _from_infliction_prob_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        inflict_param = Status(self.variant.id_a).to_buff_param_inflict()

        return self._direct_buff_unit(inflict_param, asset_manager, payload)

    def _from_affliction_punisher(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(Status(self.variant.id_a).to_buff_param_punisher(), asset_manager, payload)

    def _from_affliction_extension(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(Status(self.variant.id_a).to_buff_param_extension(), asset_manager, payload)

    def _from_fill_dragon_gauge(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.DRAGON_GAUGE_FILL, asset_manager, payload)

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
                condition_comp=payload.condition_comp + condition,
                condition_cooldown=payload.condition_cooldown,
                source_ability=payload.source_ability,
                max_occurrences=payload.max_occurrences,
                is_chained_ex=payload.is_chained_ex,
            )

            ret.update(self.to_effect_units(
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
            ret.update(self.to_effect_units(
                asset_manager.asset_action_cond.get_data_by_id(action_cond_id), payload
            ))
        return ret

    def _from_player_exp_up(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.PLAYER_EXP, asset_manager, payload)

    def _from_sp_charge(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        charge_params = {
            BuffParameter.SP_CHARGE_PCT_S1, BuffParameter.SP_CHARGE_PCT_S2,
            BuffParameter.SP_CHARGE_PCT_S3, BuffParameter.SP_CHARGE_PCT_S4
        }

        ret: set[AbilityVariantEffectUnit] = set()

        for param in charge_params:
            ret.update(self._direct_buff_unit(param, asset_manager, payload))

        return ret

    def _from_action_grant(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        action_grant_data = asset_manager.asset_action_grant.get_data_by_id(self.variant.id_a)
        action_cond_data = asset_manager.asset_action_cond.get_data_by_id(action_grant_data.action_condition_id)

        payload.target_action = action_grant_data.target_action

        units: set[AbilityVariantEffectUnit] = set(self.to_effect_units(action_cond_data, payload))
        units.update(self.to_dispel_units(action_cond_data, payload))

        return units

    def _from_combo_time_ext(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        return self._direct_buff_unit(BuffParameter.COMBO_TIME, asset_manager, payload, val_div_100=False)

    def _from_addl_heal_on_revive(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        # The parameter for the ``AssetManager`` is still needed in the signature although redundant
        # because ``_from_*`` methods are called with the same set of the parameters.

        return self._direct_buff_unit(
            BuffParameter.HEAL_INSTANT_HP, asset_manager, payload,
            addl_cond_comp=ConditionComposite(Condition.ON_REVIVED)
        )

    def get_effect_units(
            self, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
    ) -> set[AbilityVariantEffectUnit]:
        """
        Get the ability variant effect units of this ability variant.

        :raises AbilityVariantUnconvertibleError: if the variant type is not handled / unconvertible
        """
        if self.type_enum == AbilityVariantType.HIT_ATTR_SHIFT:
            return set()

        method_dict: dict[
            AbilityVariantType,
            Callable[["AssetManager", AbilityVariantEffectPayload], set[AbilityVariantEffectUnit]]
        ] = {
            AbilityVariantType.STATUS_UP: self._from_status_up,
            AbilityVariantType.DAMAGE_UP: self._from_dmg_up,
            AbilityVariantType.CRT_RATE_UP: self._from_crt_up,
            AbilityVariantType.CRT_DMG_UP: self._from_crt_dmg_up,
            AbilityVariantType.ELEM_DMG_UP: self._from_elem_dmg_up,
            AbilityVariantType.ELEM_RESIST_UP: self._from_elem_resist_up,
            AbilityVariantType.OD_GAUGE_DMG_UP: self._from_od_gauge_dmg_up,
            AbilityVariantType.RP_UP: self._from_rp_up,
            AbilityVariantType.DRAGON_DMG_UP: self._from_dragon_dmg_up,
            AbilityVariantType.BUFF_TIME_UP: self._from_buff_time_up,
            AbilityVariantType.RESISTANCE_UP: self._from_resist_up,
            AbilityVariantType.INFLICTION_PROB_UP: self._from_infliction_prob_up,
            AbilityVariantType.PLAYER_EXP_UP: self._from_player_exp_up,
            AbilityVariantType.AFFLICTION_PUNISHER: self._from_affliction_punisher,
            AbilityVariantType.AFFLICTION_EXTEND: self._from_affliction_extension,
            AbilityVariantType.FILL_DRAGON_GAUGE: self._from_fill_dragon_gauge,
            AbilityVariantType.CHANGE_STATE: self._from_change_state,
            AbilityVariantType.SP_CHARGE: self._from_sp_charge,
            AbilityVariantType.ACTION_GRANT: self._from_action_grant,
            AbilityVariantType.COMBO_TIME_EXT: self._from_combo_time_ext,
            AbilityVariantType.ADDITIONAL_HEAL_ON_REVIVE: self._from_addl_heal_on_revive
        }

        for var_type, method in method_dict.items():
            if self.type_enum == var_type:
                return method(asset_manager, payload)

        raise AbilityVariantUnconvertibleError(payload.source_ability_id, self.variant.type_id)


T = TypeVar("T", bound=AbilityEntryExtension)


def ability_to_effect_units(
        ability_entry: T, asset_manager: "AssetManager", payload: AbilityVariantEffectPayload
) -> set[AbilityVariantEffectUnit]:
    """Convert ``ability_entry`` to a set of variant effect units."""
    effect_units: set[AbilityVariantEffectUnit] = set()

    for variant in ability_entry.variants:
        if variant.type_enum == AbilityVariantType.OTHER_ABILITY:
            continue  # Refer to the other ability, no variant effect

        effect_units.update(AbilityVariantData(variant).get_effect_units(asset_manager, payload))

    return effect_units
