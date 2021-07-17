"""Classes for entries that are used in both character and dragon advanced info."""
from dataclasses import InitVar, dataclass, field
from typing import Any, Generic, TYPE_CHECKING, TypeVar

from dlparse.errors import UnhandledUnitError
from dlparse.mono.asset import CharaDataEntry, DragonDataEntry, UnitEntry
from .ability import AbilityInfoEntry
from .skill import UnitSkillEntry
from ...base import JsonExportableEntryBase, JsonSchema, UnitInfoEntryBase
from ...chara_info import CharaInfoEntry
from ...dragon_info import DragonInfoEntry
from ...skill_atk import AttackingSkillEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AdvancedInfoEntryBase",)

ET = TypeVar("ET", bound=UnitEntry)
BT = TypeVar("BT", bound=UnitInfoEntryBase)


@dataclass
class AdvancedInfoEntryBase(Generic[BT, ET], JsonExportableEntryBase):
    """An entry for the advanced info of a dragon."""

    asset_manager: InitVar["AssetManager"]
    atk_skills: InitVar[list[AttackingSkillEntry]]
    unit_data: ET

    basic: BT = field(init=False)
    skill: UnitSkillEntry = field(init=False)
    ability: AbilityInfoEntry = field(init=False)

    def __post_init__(self, asset_manager: "AssetManager", atk_skills: list[AttackingSkillEntry]):
        if isinstance(self.unit_data, CharaDataEntry):
            self.basic = CharaInfoEntry(asset_manager, self.unit_data)
        elif isinstance(self.unit_data, DragonDataEntry):
            self.basic = DragonInfoEntry(asset_manager, self.unit_data)
        else:
            raise UnhandledUnitError(self.unit_data)

        self.skill = UnitSkillEntry(asset_manager, self.unit_data, atk_skills)
        self.ability = AbilityInfoEntry(asset_manager, self.unit_data)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "type": int,
            "basic": UnitInfoEntryBase.json_schema,
            "skill": UnitSkillEntry.json_schema,
            "ability": AbilityInfoEntry.json_schema
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "type": self.unit_data.unit_type.value,
            "basic": self.basic.to_json_entry(),
            "skill": self.skill.to_json_entry(),
            "ability": self.ability.to_json_entry()
        }
