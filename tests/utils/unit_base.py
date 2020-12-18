"""Base functions for checking the units."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable, TypeVar

__all__ = ("InfoBase", "BuffInfoBase", "AbilityInfoBase", "check_info_list_match")


@dataclass
class InfoBase:
    """Base class for a partial info to match."""

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError()

    @abstractmethod
    def __lt__(self, other):
        raise NotImplementedError()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return hash(self) == hash(other)


@dataclass
class BuffInfoBase(InfoBase, ABC):
    """Base class for a buff info."""

    hit_label: str

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return self.hit_label < other.hit_label


@dataclass
class AbilityInfoBase(InfoBase, ABC):
    """Base class for an ability info."""

    source_ability_id: int

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return self.source_ability_id < other.source_ability_id


T = TypeVar("T", bound=InfoBase)


def check_info_list_match(actual_info: Iterable[T], expected_info: Iterable[T], /, message: Any = None):
    """Check if both lists of the info match."""
    expected_info: list[T] = list(sorted(expected_info))
    actual_info: list[T] = list(sorted(actual_info))

    # Message is hard-coded to let PyCharm display diff comparison tool
    expr_expected = "\\n".join([str(info) for info in expected_info])
    expr_actual = "\\n".join([str(info) for info in actual_info])

    assert_expr = f"assert [{expr_actual}] == [{expr_expected}]"

    if message is not None:
        assert_expr = f"{message}\n{assert_expr}"

    assert actual_info == expected_info, assert_expr
