"""Classes for handling the dragon data asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Element, SkillNumber, UnitType
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from dlparse.mono.asset.extension import SkillIdEntry, SkillIdentifierLabel, UnitAsset, UnitEntry

__all__ = ("DragonDataEntry", "DragonDataAsset", "DRAGON_SKILL_MAX_LEVEL")

DRAGON_SKILL_MAX_LEVEL = 2


@dataclass
class DragonDataEntry(UnitEntry, MasterEntryBase):
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

    normal_attack_action_id: int

    @property
    def icon_name(self) -> str:
        return f"{self.base_id}_{self.variation_id:02}"

    @property
    def ability_ids_all_level(self) -> list[int]:
        return [
            ability_id for ability_id in (
                self.ability_id_1_lv1, self.ability_id_1_lv2, self.ability_id_1_lv3,
                self.ability_id_1_lv4, self.ability_id_1_lv5,
                self.ability_id_2_lv1, self.ability_id_2_lv2, self.ability_id_2_lv3,
                self.ability_id_2_lv4, self.ability_id_2_lv5,
            ) if ability_id
        ]

    @property
    def has_mode_change(self) -> bool:
        return False

    @property
    def mode_ids(self) -> list[int]:
        return []

    @property
    def unit_type(self) -> UnitType:
        return UnitType.DRAGON

    @property
    def self_skill_id_entries(self) -> list[SkillIdEntry]:
        return [SkillIdEntry(self.skill_1_id, SkillNumber.S1_DRAGON, SkillIdentifierLabel.S1_DRAGON)]

    @property
    def ability_ids_at_max_level(self) -> list[int]:
        ret = [self.ability_id_1_lv5]

        if self.ability_id_2_lv5:
            ret.append(self.ability_id_2_lv5)

        return ret

    def max_skill_level(self, skill_num: SkillNumber) -> int:
        # Unique dragon is categorized as "unplayable".
        # In this case, the skill level follows unit's skill level.
        # Also, it should be parsed from chara data entry, NOT dragon data entry.
        return 2

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
            normal_attack_action_id=data["_DefaultSkill"],
            cv_en_label=data["_CvInfoEn"],
            cv_jp_label=data["_CvInfo"],
            release_date=cls.parse_datetime(data["_ReleaseStartDate"]),
            is_playable=bool(data["_IsPlayable"]),
            ss_skill_id=0,
            ss_skill_num=SkillNumber.NA,
            ss_skill_cost=0,
            unique_dragon_id=0,
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
