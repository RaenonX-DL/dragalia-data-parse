"""Classes for ability info in advanced unit info."""
from dataclasses import InitVar, dataclass, field
from typing import Any, Optional, TypeVar

from dlparse.mono.asset import CharaDataEntry, UnitEntry
from dlparse.mono.asset.extension import AbilityEntryExtension
from dlparse.mono.manager import AssetManager
from ...base import ExAbiltiesEntry, JsonExportableEntryBase, JsonSchema, TextEntry

__all__ = ("AbilityInfoEntry",)

AT = TypeVar("AT", bound=AbilityEntryExtension)


@dataclass
class OfficialAbilityInfo(JsonExportableEntryBase):
    """Entry of an official ability info."""

    asset_manager: InitVar["AssetManager"]
    ability_data: InitVar[AT]

    icon_path: str = field(init=False)
    description: TextEntry = field(init=False)

    def __post_init__(self, asset_manager: AssetManager, ability_data: AT):
        self.icon_path = ability_data.ability_icon_name
        self.description = TextEntry(
            asset_text_website=asset_manager.asset_text_website,
            asset_text_multi=asset_manager.asset_text_multi,
            labels=ability_data.description_label
        )

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "description": TextEntry.json_schema,
            "iconPath": str,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "iconPath": self.icon_path,
            "description": self.description,
        }


@dataclass
class CharaCoAbilityDataEntry(JsonExportableEntryBase):
    """An entry that collects co-ability info of a character."""

    asset_manager: InitVar["AssetManager"]
    chara_data: InitVar[CharaDataEntry]

    global_: OfficialAbilityInfo = field(init=False)
    chained: OfficialAbilityInfo = field(init=False)
    parsed: ExAbiltiesEntry = field(init=False)

    def __post_init__(self, asset_manager: AssetManager, chara_data: CharaDataEntry):
        ex_data = asset_manager.asset_ex_ability.get_data_by_id(chara_data.ex_id_at_max_level)
        self.global_ = OfficialAbilityInfo(asset_manager, ex_data)
        cex_data = asset_manager.asset_ability_data.get_data_by_id(chara_data.cex_id_at_max_level)
        self.chained = OfficialAbilityInfo(asset_manager, cex_data)
        self.parsed = ExAbiltiesEntry(asset_manager=asset_manager, unit_data=chara_data)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "global": [OfficialAbilityInfo.json_schema],
            "chained": [OfficialAbilityInfo.json_schema],
            "parsed": ExAbiltiesEntry.json_schema,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "global": self.global_,
            "chained": self.chained,
            "parsed": self.parsed,
        }


@dataclass
class AbilityInfoEntry(JsonExportableEntryBase):
    """An entry that collects all ability info of a unit."""

    asset_manager: InitVar["AssetManager"]
    unit_data: InitVar[UnitEntry]

    passive: list[OfficialAbilityInfo] = field(init=False)
    co_ability: Optional[CharaCoAbilityDataEntry] = None

    def __post_init__(self, asset_manager: AssetManager, unit_data: UnitEntry):
        self.passive = [
            OfficialAbilityInfo(asset_manager, asset_manager.asset_ability_data.get_data_by_id(ability_id))
            for ability_id in unit_data.ability_ids_at_max_level
        ]
        if isinstance(unit_data, CharaDataEntry):
            self.co_ability = CharaCoAbilityDataEntry(asset_manager, unit_data)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "passive": [OfficialAbilityInfo.json_schema],
            "coAbility": [CharaCoAbilityDataEntry.json_schema, None]
        }

    def to_json_entry(self) -> dict[str, Any]:
        ret = {
            "passive": [passive.to_json_entry() for passive in self.passive],
        }

        if self.co_ability:
            ret.update({
                "coAbility": self.co_ability.to_json_entry()
            })

        return ret
