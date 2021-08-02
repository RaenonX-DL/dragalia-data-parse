"""Interface for various types of units. This includes character and dragon."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Generic, Optional, TYPE_CHECKING, TextIO, Type, TypeVar

from dlparse.enums import Element, UnitType
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from .named import UnitNameEntry
from .skill_discovery import SkillDiscoverableEntry, SkillIdEntry
from .varied import VariedEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("UnitEntry", "UnitAsset", "SkillReverseSearchResult")


@dataclass
class UnitEntry(UnitNameEntry, VariedEntry, SkillDiscoverableEntry, MasterEntryBase, ABC):
    """Interface for an unit."""

    element: Element
    rarity: int

    cv_en_label: str
    cv_jp_label: str

    release_date: datetime

    is_playable: bool

    @property
    @abstractmethod
    def icon_name(self) -> str:
        """Get the name of the icon, excluding the file extension."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def unit_type(self) -> UnitType:
        """Unit type of this entry."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def self_skill_id_entries(self) -> list[SkillIdEntry]:
        """
        Get all skills that is the original skill.

        For example, S1 and S2 for a character; Ultimate for a dragon is the original skill.
        Note that the shared skill of a character, any phase-changed skills,
        or unique dragon skills are NOT considered as original skills.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def ability_ids_at_max_level(self) -> list[int]:
        """Get the ability IDs at its max level."""
        raise NotImplementedError()


@dataclass
class SkillReverseSearchResult:
    """Result class of the skill -> unit reverse search."""

    unit_data: UnitEntry
    skill_id_entry: SkillIdEntry


T = TypeVar("T", bound=UnitEntry)


class UnitAsset(Generic[T], MasterAssetBase[T], ABC):
    """Interface for an asset that contains unit entries."""

    def __init__(
            self, parser_cls: Type[MasterParserBase[T]], file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(parser_cls, file_location, asset_dir=asset_dir, file_like=file_like)

        # Cache for getting the unit data by skill ID
        self._cache_skill_id: dict[int, SkillReverseSearchResult] = {}  # K = skill ID, V = reverse search result
        self._traversed_unit_id: set[int] = set()

    def get_unit_data_by_skill_id(
            self, asset_manager: "AssetManager", skill_id: int, /,
            playable_only: bool = True, is_dragon: bool = False,
    ) -> Optional[SkillReverseSearchResult]:
        """
        Get the unit data whose any of the skill is ``skill_id``.

        Returns ``None`` if none of the unit data has a skill of ``skill_id``.
        """
        # Get the result from the cache, if exists
        if skill_id in self._cache_skill_id:
            return self._cache_skill_id[skill_id]

        # Traverse all un-traversed unit data
        # - Traversed results will be stored in the cache
        unit_data: UnitEntry
        for unit_data in filter(lambda data: data.id not in self._traversed_unit_id, self):
            # Record that the unit data has been traversed
            self._traversed_unit_id.add(unit_data.id)

            # Don't continue if ``playable_only`` and the unit is not playable
            if playable_only and not unit_data.is_playable:
                continue

            # Get the skill ID entries
            entries = unit_data.get_skill_id_entries(asset_manager, is_dragon=is_dragon)

            # Store each result to the cache
            for entry in entries:
                self._cache_skill_id[entry.skill_id] = SkillReverseSearchResult(
                    unit_data=unit_data, skill_id_entry=entry
                )

            # Return if the data is stored in the cache (found in the previous code)
            if skill_id in self._cache_skill_id:
                return self._cache_skill_id[skill_id]

        # Unit data not found, returns ``None``
        return None

    @property
    def playable_data(self) -> list[T]:
        """Get all playable units.."""
        return [data for data in self if data.is_playable]
