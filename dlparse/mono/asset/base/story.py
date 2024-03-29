"""Base entry class of a story."""
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Generic, Optional, TextIO, Type, TypeVar

from .master import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("StoryEntryBase", "GroupedStoryEntryBase", "GroupedStoryAssetBase")


@dataclass
class StoryEntryBase(MasterEntryBase, ABC):
    """Base class of a story entry."""

    title_label: str


@dataclass
class GroupedStoryEntryBase(StoryEntryBase, ABC):
    """Base class of a grouped story entry."""

    group_id: int


T = TypeVar("T", bound=GroupedStoryEntryBase)


class GroupedStoryAssetBase(Generic[T], MasterAssetBase[T], ABC):
    """Base class for an asset containing grouped story entries."""

    def _init_lookup_by_group_id(self):
        for entry in self.data.values():
            self._lookup_by_group_id[entry.group_id].append(entry)

    def __init__(
            self, parser_cls: Type[MasterParserBase[T]], file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(parser_cls, file_location, asset_dir=asset_dir, file_like=file_like)

        self._lookup_by_group_id: dict[int, list[T]] = defaultdict(list)
        self._init_lookup_by_group_id()

    def get_data_by_group_id(self, group_id: int) -> Optional[list[T]]:
        """Get the story entries that is grouped under ``group_id``."""
        return self._lookup_by_group_id.get(group_id)
