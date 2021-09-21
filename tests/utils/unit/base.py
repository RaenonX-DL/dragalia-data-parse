"""Base functions for checking the units."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import zip_longest
from typing import Any, Iterable, TypeVar, final

__all__ = ("InfoBase", "BuffInfoBase", "AbilityInfoBase", "check_info_list_match")


@dataclass(eq=False)
class InfoBase:
    """Base class for a partial info to match."""

    @property
    @abstractmethod
    def _comparer(self) -> tuple[Any, ...]:
        raise NotImplementedError()

    @final
    def __hash__(self) -> int:
        return hash(self._comparer)

    @final
    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return self._comparer < other._comparer

    @final
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self._comparer == other._comparer


@dataclass(eq=False)
class BuffInfoBase(InfoBase, ABC):
    """Base class for a buff info."""

    hit_label: str

    @property
    def _comparer(self) -> tuple[Any, ...]:
        return self.hit_label,


@dataclass(eq=False)
class AbilityInfoBase(InfoBase, ABC):
    """Base class for an ability info."""

    source_ability_id: int

    @property
    def _comparer(self) -> tuple[Any, ...]:
        return self.source_ability_id,


T = TypeVar("T", bound=InfoBase)


def check_info_list_match(
        actual_info: Iterable[T], expected_info: Iterable[T], /,
        message: Any = None
) -> None:
    """Check if both lists of the info match."""
    expected_info: list[T] = list(sorted(expected_info))
    actual_info: list[T] = list(sorted(actual_info))

    # Message is hard-coded to let PyCharm display diff comparison tool
    expr_expected = "\\n".join([str(info) for info in expected_info])
    expr_actual = "\\n".join([str(info) for info in actual_info])

    assert_expr = f"assert [{expr_actual}] == [{expr_expected}]"

    if message is not None:
        assert_expr = f"{message}\n{assert_expr}"

    for idx, (actual, expected) in enumerate(zip_longest(actual_info, expected_info)):
        assert actual == expected, f"{assert_expr}\nIndex #{idx} not equal"  # nosec
