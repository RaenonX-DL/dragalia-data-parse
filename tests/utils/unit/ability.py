"""Implementations for checking the affliction effects."""
from dataclasses import dataclass, field
from typing import Any, Optional, TypeVar

import pytest

from dlparse.enums import AbilityTargetAction, BuffParameter, ConditionComposite, HitTargetSimple
from dlparse.model import AbilityDataBase, AbilityVariantEffectUnit
from dlparse.mono.asset import CharaDataEntry
from .base import AbilityInfoBase, check_info_list_match

__all__ = (
    "AbilityEffectInfo", "UnknownAbilityData", "UnknownAbilityDataCollection", "check_ability_effect_unit_match"
)


@dataclass(eq=False)
class AbilityEffectInfo(AbilityInfoBase):
    """A single affliction info entry."""

    condition_comp: ConditionComposite
    parameter: BuffParameter
    rate: float
    probability: Optional[float] = None
    cooldown_sec: Optional[float] = None
    max_occurrences: Optional[int] = None
    max_stack_count: Optional[int] = None
    target: Optional[HitTargetSimple] = None
    target_action: Optional[AbilityTargetAction] = None
    duration_sec: Optional[float] = None
    duration_count: Optional[float] = None
    slip_interval_sec: Optional[float] = None

    @property
    def _comparer(self) -> tuple[Any, ...]:
        return (
            self.source_ability_id,
            self.condition_comp.conditions_sorted,
            int(self.parameter.value),
            int(round(self.rate * 1E5))
        )


def check_ability_effect_unit_match(
        actual_units: set[AbilityVariantEffectUnit], expected_info: set[AbilityEffectInfo], /,
        message: Any = None
) -> None:
    """Check if the info of the affliction units match."""
    # Explicit ``None`` checks because ``0`` is falsy
    has_probability = any(info.probability is not None for info in expected_info)
    has_cooldown = any(info.cooldown_sec is not None for info in expected_info)
    has_max_occurrences = any(info.max_occurrences is not None for info in expected_info)
    has_max_stack = any(info.max_stack_count is not None for info in expected_info)
    has_target = any(info.target is not None for info in expected_info)
    has_target_action = any(info.target_action is not None for info in expected_info)
    has_duration_sec = any(info.duration_sec is not None for info in expected_info)
    has_duration_count = any(info.duration_count is not None for info in expected_info)
    has_slip_interval = any(info.slip_interval_sec is not None for info in expected_info)

    actual_info = [
        AbilityEffectInfo(
            source_ability_id=unit.source_ability_id,
            condition_comp=unit.condition_comp,
            parameter=unit.parameter,
            rate=unit.rate,
            probability=unit.probability_pct if has_probability else None,
            cooldown_sec=unit.cooldown_sec if has_cooldown else None,
            max_occurrences=unit.max_occurrences if has_max_occurrences else None,
            max_stack_count=unit.max_stack_count if has_max_stack else None,
            target=unit.target if has_target else None,
            target_action=unit.target_action if has_target_action else None,
            duration_sec=unit.duration_sec if has_duration_sec else None,
            duration_count=unit.duration_count if has_duration_count else None,
            slip_interval_sec=unit.slip_interval_sec if has_slip_interval else None,
        )
        for unit in actual_units
    ]

    check_info_list_match(actual_info, expected_info, message=message)


@dataclass(eq=False)
class UnknownAbilityData:
    """A single unknown ability data entry."""

    chara_id: int
    ability_id: int

    condition_ids: dict[int, int]
    variant_ids: dict[int, list[int]]

    error: Optional[Exception] = None

    is_empty: bool = False
    not_effective_to_the_team: bool = False

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        ret = f"- #{self.ability_id} ({self.chara_id})"

        for source_ab_id, condition_id in self.condition_ids.items():
            ret += f"\n  - Condition ID: {condition_id} from #{source_ab_id}"

        for source_ab_id, variant_type_ids in self.variant_ids.items():
            ret += f"\n  - Variant type IDs: {variant_type_ids} from #{source_ab_id}"

        if self.error:
            ret += f"\n  - Error: {self.error}"

        if self.is_empty:
            ret += "\n  - Empty effect"

        if self.not_effective_to_the_team:
            ret += "\n  - Not effective to the whole team"

        return ret


T = TypeVar("T", bound=AbilityDataBase)


@dataclass
class UnknownAbilityDataCollection:
    """A holder class for the unknown ability data."""

    data: list[UnknownAbilityData] = field(init=False, default_factory=list)

    def add_data(self, unknown_info: UnknownAbilityData) -> None:
        """Add ``unknown_info`` to the data to be printed later."""
        self.data.append(unknown_info)

    def add_data_if_needed(
            self, chara_data: CharaDataEntry, ability_id: int, ability_data: T, /,
            check_effective_for_team: bool = False
    ) -> None:
        """Record that ``ability_data`` has unknown data, if any."""
        # Check if any unknown elements exist but no error yielded
        if ability_data.has_unknown_elements:
            self.add_data(UnknownAbilityData(
                chara_id=chara_data.id, ability_id=ability_id,
                condition_ids=ability_data.unknown_condition_ids,
                variant_ids=ability_data.unknown_variant_ids
            ))

        # Ability should be effective to the whole team
        if not ability_data.effect_units:
            self.add_data(UnknownAbilityData(
                chara_id=chara_data.id, ability_id=ability_id, is_empty=True,
                condition_ids=ability_data.unknown_condition_ids,
                variant_ids=ability_data.unknown_variant_ids
            ))

        # Ability should be effective to the whole team
        if check_effective_for_team and any(unit.target != HitTargetSimple.TEAM for unit in ability_data.effect_units):
            self.add_data(UnknownAbilityData(
                chara_id=chara_data.id, ability_id=ability_id, not_effective_to_the_team=True,
                condition_ids=ability_data.unknown_condition_ids,
                variant_ids=ability_data.unknown_variant_ids
            ))

    def print_and_fail_if_any(self, total_data_count: int) -> None:
        """Print the unknown ability data and fail the test, if any of the unknown data is present"""
        if self.data:
            unknown_str = "\n".join([str(entry) for entry in self.data])
            pytest.fail(
                f"{len(self.data)} abilities have unknown elements "
                f"(total {total_data_count}, {1 - len(self.data) / total_data_count:.2%} parsed):\n"
                f"{unknown_str}"
            )
