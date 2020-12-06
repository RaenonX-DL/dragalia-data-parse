"""Base functions for checking the units."""
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar


@dataclass
class BuffInfoBase:
    """Base class for buff info."""

    hit_label: str

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return self.hit_label < other.hit_label


T = TypeVar("T", bound=BuffInfoBase)


def check_info_list_match(actual_info: list[T], expected_info: list[T], /, message: Any = None):
    """Check if both lists of the info match."""
    # Message is hard-coded to let PyCharm display diff comparison tool
    expr_expected = "\\n".join([str(info) for info in sorted(expected_info)])
    expr_actual = "\\n".join([str(info) for info in sorted(actual_info)])

    assert_expr = f"assert [{expr_actual}] == [{expr_expected}]"

    if message is not None:
        assert_expr = f"{message}\n{assert_expr}"

    assert actual_info == expected_info, assert_expr
