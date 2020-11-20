"""Base object for the player action assets."""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Optional, Callable, Union, ClassVar

from .asset import AssetBase
from .entry import EntryBase
from .parser import ParserBase

__all__ = (
    "ActionComponentBase", "ActionComponentDamageDealerMixin",
    "ActionAssetBase",
    "ActionParserBase"
)


@dataclass
class ActionComponentCondition(EntryBase):
    """Condition data of an action component."""

    type_id: int
    type_values: list[int]

    @staticmethod
    def parse_raw(data: dict[str, Union[int, list[int]]]) -> Optional["ActionComponentCondition"]:
        if data.get("_conditionType", 0):
            return None

        return ActionComponentCondition(
            type_id=data["_conditionType"],
            type_values=data["_conditionValue"]
        )


@dataclass
class ActionComponentLoop(EntryBase):
    """Loop data of an action component."""

    loop_count: int
    restart_frame: int
    restart_sec: float

    @staticmethod
    def parse_raw(data: dict[str, Union[int, float]]) -> Optional["ActionComponentLoop"]:
        if data.get("flag", 0):
            return None

        return ActionComponentLoop(
            loop_count=data["loopNum"],
            restart_frame=data["restartFrame"],
            restart_sec=data["restartSec"]
        )


@dataclass
class ActionComponentBase(EntryBase, ABC):
    """Base class for the components in the player action mono behavior asset."""

    command_type_id: int

    speed: float

    time_start: float
    time_duration: float

    condition_data: Optional[ActionComponentCondition]
    loop_data: Optional[ActionComponentLoop]

    @staticmethod
    @abstractmethod
    def parse_raw(data: dict[str, Union[str, int, float]]) -> "ActionComponentBase":
        """Parse a raw data to be the component class."""
        raise NotImplementedError()

    @classmethod
    def get_base_kwargs(cls, raw_data: dict[str, Union[str, int, float, dict[str, Union[int, float]]]]) \
            -> dict[str, Union[int, float, Optional[ActionComponentCondition], Optional[ActionComponentLoop]]]:
        """Get the base kwargs for constructing the component."""
        return {
            "command_type_id": raw_data["commandType"],
            "speed": raw_data["_speed"],
            "time_start": raw_data["_seconds"],
            "time_duration": raw_data["_duration"],
            "condition_data": ActionComponentCondition.parse_raw(raw_data["_conditionData"]),
            "loop_data": ActionComponentLoop.parse_raw(raw_data["_loopData"])
        }


@dataclass
class ActionComponentDamageDealerMixin(EntryBase, ABC):
    """
    Mixin class for damage dealing components.

    A damage dealing component should have hit label(s) assigned.
    """

    # pylint: disable=invalid-name
    NON_DAMAGE_DEALING_LABELS: ClassVar[set[str]] = {
        "CMN_AVOID"
    }

    hit_labels: list[str]


class ActionParserBase(ParserBase, ABC):
    """Base parser class for parsing the player action asset files."""

    @staticmethod
    def get_components(file_path: str) -> list[dict]:
        """Get a list of components as raw data, which needs to be further parsed."""
        with open(file_path) as f:
            data = json.load(f)

        if "Components" not in data:
            raise ValueError("Key `Components` not in the data")

        return data["Components"]

    @staticmethod
    def parse_file(file_path: str) -> list[ActionComponentBase]:
        """Parse a file as a list of components."""
        raise NotImplementedError()


class ActionAssetBase(AssetBase, ABC):
    """Base class for a player action mono behavior asset."""

    def __init__(self, parser_cls: Type[ActionParserBase], file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(parser_cls, file_path, asset_dir=asset_dir)

    def __iter__(self):
        return iter(self._data)

    def filter(self, condition: Callable[[ActionComponentBase], bool]) -> list[ActionComponentBase]:
        """Get a list of components which matches the ``condition``."""
        return [data for data in self if condition(data)]
