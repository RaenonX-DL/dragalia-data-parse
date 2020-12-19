"""Base classes for the data entries to be exported."""
import hashlib
from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass, field
from typing import Generic, TYPE_CHECKING, TypeVar, final

from dlparse.enums import ConditionComposite, Element, SkillNumber

if TYPE_CHECKING:
    from dlparse.mono.asset import CharaDataEntry, SkillDataEntry, SkillIdEntry, TextAsset

__all__ = ("ExportEntryBase", "SkillExportEntryBase")


class ExportEntryBase(ABC):
    """Base class for an exported data entry."""

    @property
    @abstractmethod
    def unique_id(self) -> str:
        """An ID that uniquely identifies the entry."""
        raise NotImplementedError()

    @property
    @final
    def unique_hash(self):
        """A hash that uniquely identifies this entry."""
        return hashlib.sha256(self.unique_id.encode("utf-8")).hexdigest()

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        raise NotImplementedError(f"Entry `{self.__class__.__name__}` cannot be converted to a csv entry")

    @classmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file containing this entry."""
        raise NotImplementedError(f"Entry `{cls.__name__}` does not implement a csv header")


T = TypeVar("T")


@dataclass
class SkillExportEntryBase(Generic[T], ExportEntryBase, ABC):
    """Base class for an exported skill data entry."""

    text_asset: InitVar["TextAsset"]

    chara_data: InitVar["CharaDataEntry"]

    skill_data: InitVar["SkillDataEntry"]

    skill_id_entry: InitVar["SkillIdEntry"]

    condition_comp: ConditionComposite

    skill_data_to_parse: InitVar[T]

    character_custom_id: str = field(init=False)
    character_name: str = field(init=False)
    character_internal_id: int = field(init=False)
    character_element: Element = field(init=False)

    skill_internal_id: int = field(init=False)
    skill_identifiers: str = field(init=False)
    skill_num: SkillNumber = field(init=False)
    skill_name: str = field(init=False)
    skill_max_level: int = field(init=False)

    sp_at_max: float = field(init=False)
    sharable: bool = field(init=False)
    ss_cost: int = field(init=False)
    ss_sp: float = field(init=False)

    def __post_init__(self, text_asset: "TextAsset", chara_data: "CharaDataEntry", skill_data: "SkillDataEntry",
                      skill_id_entry: "SkillIdEntry", skill_data_to_parse: T):  # pylint: disable=unused-argument
        self.character_custom_id = chara_data.custom_id
        self.character_name = chara_data.get_chara_name(text_asset)
        self.character_internal_id = chara_data.id
        self.character_element = chara_data.element

        self.skill_internal_id = skill_id_entry.skill_id
        self.skill_identifiers = skill_id_entry.skill_identifier_labels
        self.skill_num = skill_id_entry.skill_num
        self.skill_name = text_asset.to_text(skill_data.name_label, silent_fail=False)
        self.skill_max_level = chara_data.max_skill_level(skill_id_entry.skill_num)

        self.sp_at_max = skill_data.get_sp_at_level(self.skill_max_level)
        self.sharable = chara_data.ss_skill_id == skill_data.id
        self.ss_cost = chara_data.ss_skill_cost
        self.ss_sp = skill_data.get_ss_sp_at_level(self.skill_max_level) if self.sharable else 0

    @property
    def unique_id(self) -> str:
        return (
            f"{self.character_internal_id}{self.skill_internal_id}{self.skill_identifiers}"
            f"{hash(self.condition_comp)}"
        )

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        return [
            self.unique_hash,
            self.character_custom_id,
            self.character_name,
            self.character_internal_id,
            self.character_element,
            self.skill_internal_id,
            self.skill_identifiers,
            self.condition_comp,
            self.sp_at_max,
            self.ss_sp
        ]

    @classmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file."""
        return [
            "Entry Hash",
            "Character ID",
            "Character Name",
            "Character Internal ID",
            "Character Element",
            "Skill Internal ID",
            "Skill Identifier",
            "Conditions",
            "SP (at max lv)",
            "SS SP (at max lv)"
        ]
