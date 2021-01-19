"""Base classes for condition-related classes."""
from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass
from enum import Enum
from typing import Generic, Iterable, Optional, Sequence, TypeVar, Union

__all__ = ("ConditionCompositeBase", "ConditionCheckResultMixin")

T = TypeVar("T", bound=Enum)


class ConditionCheckResultMixin:
    """Mixin class for condition checking result."""

    def __bool__(self):
        return self.passed

    @property
    def passed(self):
        """If the check result means the check has passed."""
        return self in self.passing_enums()

    @classmethod
    @abstractmethod
    def passing_enums(cls) -> set[Enum]:
        """A :class:`set` of :class:`Enum` which means the check has passed."""
        raise NotImplementedError()


@dataclass
class ConditionCompositeBase(Generic[T], ABC):
    """Base condition composite class."""

    conditions: InitVar[Optional[Union[Iterable[T], T]]] = None

    @classmethod
    def _init_process_conditions(cls, conditions: Optional[Union[Iterable[T], T]]) -> tuple[T]:
        """
        This processes ``conditions`` and validates it.

        The processing includes forcing the data type of ``conditions`` to be a :class:`tuple`.
        """
        if isinstance(conditions, Enum):
            # Cast the condition to be a list to generalize the data type
            conditions = (conditions,)
        elif isinstance(conditions, list):
            # Cast the condition to be a tuple (might be :class:`list` when passed in)
            conditions = tuple(conditions)
        elif not conditions:
            # Conditions is either empty sequence or ``None``
            conditions = ()

        cls._init_validate_conditions(conditions)

        return conditions

    @staticmethod
    @abstractmethod
    def _init_validate_conditions(conditions: tuple[T]):
        raise NotImplementedError()

    def __hash__(self):
        return hash(tuple(sorted(condition.value for condition in self.conditions_sorted)))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"{{{', '.join({condition.name for condition in self.conditions_sorted})}}}"

    def __contains__(self, item):
        return item in self.conditions_sorted

    @abstractmethod
    def __post_init__(self, conditions: Optional[Union[Sequence[T], T]]):
        raise NotImplementedError()

    @property
    @abstractmethod
    def conditions_sorted(self) -> tuple[T]:
        """
        Get the sorted conditions as a tuple.

        This method should not be changed frequently, because the order will affect the hash of this composite.
        """
        raise NotImplementedError()
