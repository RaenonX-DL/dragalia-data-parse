"""
Classes for handling the quest data asset.

Note that enemy data and enemy param are different things.
"""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Element, Status
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("EnemyParamEntry", "EnemyParamAsset")


@dataclass
class EnemyParamEntry(MasterEntryBase):
    """Single entry of an enemy param data."""

    enemy_data_id: int

    ai_name: str
    action_set_id: int
    action_set_id_on_elem: dict[Element, int]

    ability_ids: list[int]
    ability_berserk_id: int

    hp: int
    atk: int
    defense: int

    base_od: int
    base_bk: int

    affliction_resistance_pct: dict[Status, int]

    form_2nd_param_id: int

    child_1_param_id: int
    child_1_count: int
    child_2_param_id: int
    child_2_count: int
    child_3_param_id: int
    child_3_count: int

    part_1_param_id: int
    part_2_param_id: int
    part_3_param_id: int
    part_4_param_id: int

    appear_voice_id: str

    @staticmethod
    def get_affliction_resistance_pct(data: dict[str, Union[str, int]]) -> dict[Status, int]:
        """
        Get a dictionary which key is the corresponding abnormal status; value is its corresponding resistance.

        Note that the value returning is percentage (%). A value of 100 means absolute resist.
        """
        ret = {
            Status.POISON: data["_RegistAbnormalRate01"],
            Status.BURN: data["_RegistAbnormalRate02"],
            Status.FREEZE: data["_RegistAbnormalRate03"],
            Status.PARALYZE: data["_RegistAbnormalRate04"],
            Status.BLIND: data["_RegistAbnormalRate05"],
            Status.STUN: data["_RegistAbnormalRate06"],
            Status.CURSE: data["_RegistAbnormalRate07"],
            Status.BOG: data["_RegistAbnormalRate08"],
            Status.SLEEP: data["_RegistAbnormalRate09"],
            Status.FROSTBITE: data["_RegistAbnormalRate10"],
            Status.FLASHBURN: data["_RegistAbnormalRate11"],
            Status.STORMLASH: data["_RegistAbnormalRate12"],
            Status.SHADOWBLIGHT: data["_RegistAbnormalRate13"],
            Status.SCORCHREND: data["_RegistAbnormalRate14"],
        }

        return ret

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "EnemyParamEntry":
        action_set_id_elem = {
            Element.FLAME: data["_ActionSetFire"],
            Element.WATER: data["_ActionSetWater"],
            Element.WIND: data["_ActionSetWind"],
            Element.LIGHT: data["_ActionSetLight"],
            Element.SHADOW: data["_ActionSetDark"],
        }

        ability_ids = [
            data["_Ability01"],
            data["_Ability02"],
            data["_Ability03"],
            data["_Ability04"]
        ]

        return EnemyParamEntry(
            id=data["_Id"],
            enemy_data_id=data["_DataId"],
            ai_name=data["_Ai"],
            action_set_id=data["_ActionSet"],
            action_set_id_on_elem=action_set_id_elem,
            ability_ids=ability_ids,
            ability_berserk_id=data["_BerserkAbility"],
            hp=data["_HP"],
            atk=data["_Atk"],
            defense=data["_Def"],
            base_od=data["_BaseOD"],
            base_bk=data["_BaseBreak"],
            affliction_resistance_pct=EnemyParamEntry.get_affliction_resistance_pct(data),
            form_2nd_param_id=data["_Form2nd"],
            child_1_param_id=data["_Child01Param"],
            child_1_count=data["_Child01Num"],
            child_2_param_id=data["_Child02Param"],
            child_2_count=data["_Child02Num"],
            child_3_param_id=data["_Child03Param"],
            child_3_count=data["_Child03Num"],
            part_1_param_id=data["_PartsA"],
            part_2_param_id=data["_PartsB"],
            part_3_param_id=data["_PartsC"],
            part_4_param_id=data["_PartsD"],
            appear_voice_id=data["_BossAppearVoiceId"],
        )


class EnemyParamAsset(MasterAssetBase[EnemyParamEntry]):
    """Enemy param asset class."""

    asset_file_name = "EnemyParam.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(EnemyParamParser, file_location, asset_dir=asset_dir, file_like=file_like)


class EnemyParamParser(MasterParserBase[EnemyParamEntry]):
    """Class to parse the enemy param data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, EnemyParamEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: EnemyParamEntry.parse_raw(value) for key, value in entries.items()}
