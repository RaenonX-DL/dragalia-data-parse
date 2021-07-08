"""Base object for the player action assets."""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional, TextIO, Type, Union

from dlparse.enums import ActionConditionType, Condition, ConditionCategories
from dlparse.errors import AssetKeyMissingError
from .asset import AssetBase
from .entry import EntryBase
from .parser import ParserBase

__all__ = (
    "ActionComponentBase", "ActionComponentHasHitLabels", "ActionComponentCondition",
    "ActionAssetBase", "ActionParserBase", "ActionComponentData"
)

ActionComponentData = dict[str, Union[int, str, dict[str, str], list[str]]]


@dataclass
class ActionComponentCondition(EntryBase):
    """Condition data of an action component."""

    type_condition: ActionConditionType
    type_values: list[int]

    @staticmethod
    def parse_raw(data: dict[str, Union[int, list[int]]]) -> Optional["ActionComponentCondition"]:
        return ActionComponentCondition(
            type_condition=ActionConditionType(data["_conditionType"]),
            type_values=data["_conditionValue"]
        )

    @property
    def _pre_condition_action_cond_count(self) -> Condition:
        # Appears in Nevin S2 (103505042 - 391330)
        if self.type_values[0] == 1152:
            if self.type_values[2] == 1:
                return Condition.SELF_SIGIL_LOCKED
            if self.type_values[2] == 0:
                return Condition.SELF_SIGIL_RELEASED

        return Condition.NONE

    @property
    def _pre_condition_shikigami_level(self) -> Condition:
        # Appears in Seimei S2 (107501042 - 791270)
        if self.type_values[1] == 1:
            return Condition.SELF_SEIMEI_SHIKIGAMI_LV_1
        if self.type_values[1] == 2:
            return Condition.SELF_SEIMEI_SHIKIGAMI_LV_2

        return Condition.NONE

    @property
    def skill_pre_condition(self) -> Condition:
        """Get the action executing pre-condition."""
        if self.type_condition == ActionConditionType.ACTION_CONDITION_COUNT:
            return self._pre_condition_action_cond_count
        elif self.type_condition == ActionConditionType.SEIMEI_SHIKIGAMI_LEVEL:
            return self._pre_condition_shikigami_level
        elif self.type_condition == ActionConditionType.ACTION_CANCEL:
            return ConditionCategories.skill_action_cancel.convert_reversed(self.type_values[0])

        return Condition.NONE


@dataclass
class ActionComponentLoop(EntryBase):
    """Loop data of an action component."""

    loop_count: int
    restart_frame: int
    restart_sec: float

    @staticmethod
    def parse_raw(data: dict[str, Union[int, float]]) -> Optional["ActionComponentLoop"]:
        if not data.get("flag", 0):
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

    @property
    def skill_pre_condition(self) -> Condition:
        """Get the pre-condition for this action component to be executed."""
        if not self.condition_data:
            return Condition.NONE

        return self.condition_data.skill_pre_condition

    @staticmethod
    @abstractmethod
    def parse_raw(data: dict[str, Union[str, int, float]]) -> "ActionComponentBase":
        """Parse a raw data to be the component class."""
        raise NotImplementedError()

    @classmethod
    def get_base_kwargs(
            cls, raw_data: dict[str, Union[str, int, float, dict[str, Union[int, float]]]]
    ) -> dict[str, Union[int, float, ActionComponentCondition, ActionComponentLoop, list[str], None]]:
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
class ActionComponentHasHitLabels(ActionComponentBase, ABC):
    """Base class for action components which have hit labels assigned."""

    hit_labels: list[str]

    use_same_component: bool
    """
    This indicates if the hit labels of the action component is shared across the levels.

    That is, if this is ``True``, only the hit label which ends with ``LV01`` will be used.
    For skill level 2, the same action component will be used.

    To get the hit label for level 2, just let the label ends with ``LV02``.

    If this is ``False``, then hit label = ``DAG_131_04_PLUS_H02_LV01`` is for only level 1.

    For example, if this is ``True``, tags like ``DAG_131_04_PLUS_H02_LV01``
    will appear in the component to represent all hit labels across the levels
    (we can say that label root = ``DAG_131_04_PLUS_H02``);
    if this is ``False``, ``DAG_131_04_PLUS_H02_LV01`` only works for level 1.

    .. note::
        Currently known case of this being ``False``:

        - :class:`ActionBulletFormation`
    """

    def __post_init__(self):
        # Some labels contain whitespaces, check the doc of the test ``test_label_has_whitespaces()``
        self.hit_labels = [label.strip() for label in self.hit_labels]

    @classmethod
    def get_base_kwargs(
            cls, raw_data: dict[str, Union[str, int, float, dict[str, Union[int, float]]]]
    ) -> dict[str, Union[int, float, ActionComponentCondition, ActionComponentLoop, list[str], None]]:
        base_kwargs = super().get_base_kwargs(raw_data)

        base_kwargs["use_same_component"] = bool(raw_data.get("_useSameComponent", 1))

        return base_kwargs


class ActionParserBase(ParserBase, ABC):
    """Base parser class for parsing the player action asset files."""

    @staticmethod
    def get_components(file_like: TextIO) -> list[dict]:
        """
        Get a list of components as raw data, which needs to be further parsed.

        :raises AssetKeyMissingError: if key `Components` is not in the data
        """
        data = json.load(file_like)

        if "Components" not in data:
            raise AssetKeyMissingError("Components")

        return data["Components"]

    @staticmethod
    def parse_file(file_like: str) -> list[ActionComponentBase]:
        """Parse a file as a list of components."""
        raise NotImplementedError()


class ActionAssetBase(AssetBase, ABC):
    """Base class for a player action mono behavior asset."""

    def __init__(
            self, parser_cls: Type[ActionParserBase], file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None
    ):
        super().__init__(parser_cls, file_location, asset_dir=asset_dir)

    def __iter__(self):
        return iter(self._data)

    def filter(self, condition: Callable[[ActionComponentBase], bool]) -> list[ActionComponentBase]:
        """Get a list of components which matches the ``condition``."""
        return [data for data in self if condition(data)]
