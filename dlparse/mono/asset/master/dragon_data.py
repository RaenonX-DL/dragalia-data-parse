"""Classes for handling the dragon data asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Element
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from dlparse.mono.asset.extension import SkillEntry, UnitAsset, UnitEntry, VariedEntry

__all__ = ("DragonDataEntry", "DragonDataAsset", "DRAGON_SKILL_MAX_LEVEL")

DRAGON_SKILL_MAX_LEVEL = 2


@dataclass
class DragonDataEntry(UnitEntry, VariedEntry, SkillEntry, MasterEntryBase):
    """Single entry of a dragon data."""

    ability_id_1_lv1: int
    ability_id_1_lv2: int
    ability_id_1_lv3: int
    ability_id_1_lv4: int
    ability_id_1_lv5: int
    ability_id_2_lv1: int
    ability_id_2_lv2: int
    ability_id_2_lv3: int
    ability_id_2_lv4: int
    ability_id_2_lv5: int

    @property
    def icon_name(self) -> str:
        return f"{self.base_id}_{self.variation_id:02}"

    @classmethod
    def parse_raw(cls, data: dict[str, Union[str, int]]) -> "DragonDataEntry":
        return DragonDataEntry(
            id=data["_Id"],
            emblem_id=data["_EmblemId"],
            element=Element(data["_ElementalType"]),
            rarity=data["_Rarity"],
            name_label=data["_Name"],
            name_label_2=data["_SecondName"],
            base_id=data["_BaseId"],
            variation_id=data["_VariationId"],
            skill_1_id=data["_Skill1"],
            skill_2_id=data["_Skill2"],
            ability_id_1_lv1=data["_Abilities11"],
            ability_id_1_lv2=data["_Abilities12"],
            ability_id_1_lv3=data["_Abilities13"],
            ability_id_1_lv4=data["_Abilities14"],
            ability_id_1_lv5=data["_Abilities15"],
            ability_id_2_lv1=data["_Abilities21"],
            ability_id_2_lv2=data["_Abilities22"],
            ability_id_2_lv3=data["_Abilities23"],
            ability_id_2_lv4=data["_Abilities24"],
            ability_id_2_lv5=data["_Abilities25"],
            cv_en_label=data["_CvInfoEn"],
            cv_jp_label=data["_CvInfo"],
            release_date=cls.parse_datetime(data["_ReleaseStartDate"]),
            is_playable=bool(data["_IsPlayable"])
        )


class DragonDataAsset(UnitAsset[DragonDataEntry], MasterAssetBase[DragonDataEntry]):
    """Dragon data asset class."""

    asset_file_name = "DragonData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(DragonDataParser, file_location, asset_dir=asset_dir, file_like=file_like)


class DragonDataParser(MasterParserBase[DragonDataEntry]):
    """Class to parse the dragon data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, DragonDataEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: DragonDataEntry.parse_raw(value) for key, value in entries.items()}
