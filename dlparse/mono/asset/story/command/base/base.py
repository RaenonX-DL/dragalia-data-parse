from abc import ABC
from dataclasses import InitVar, dataclass, field

from dlparse.enums import StoryCommandType
from .typedef import RawCommand

__all__ = ("StoryCommandBase",)


@dataclass
class StoryCommandBase(ABC):
    """A class representing a single command in a story."""

    raw_command: InitVar[RawCommand]

    row: int = field(init=False)
    command: StoryCommandType = field(init=False)
    command_raw: str = field(init=False)
    args: list[str] = field(init=False)

    def __post_init__(self, raw_command: RawCommand) -> None:
        self.row = raw_command["row"]
        self.command = StoryCommandType(raw_command["command"])
        self.command_raw = raw_command["command"]
        self.args = raw_command["args"]
