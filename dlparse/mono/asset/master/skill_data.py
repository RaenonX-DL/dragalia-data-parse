"""Classes for handling the skill data asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("SkillDataEntry", "SkillDataAsset", "SkillDataParser")

SKILL_MAX_LEVEL = 4


@dataclass
class SkillDataEntry(MasterEntryBase):
    """Single entry of a skill data."""

    name_label: str

    skill_type_id: int

    icon_lv1_label: str
    icon_lv2_label: str
    icon_lv3_label: str
    icon_lv4_label: str
    description_lv1_label: str
    description_lv2_label: str
    description_lv3_label: str
    description_lv4_label: str

    sp_lv1: int
    sp_lv2: int
    sp_lv3: int
    sp_lv4: int

    sp_ss_lv1: int
    sp_ss_lv2: int
    sp_ss_lv3: int
    sp_ss_lv4: int

    sp_dragon_lv1: int
    sp_dragon_lv2: int
    sp_dragon_lv3: int
    sp_dragon_lv4: int

    sp_gauge_count: int

    required_buff_id: int
    required_buff_count: int

    action_1_id: int
    action_2_id: int
    action_3_id: int
    action_4_id: int

    adv_skill_lv1: int
    """Skill level enhancement after 50 MC."""
    adv_skill_lv1_action_id: int
    """Action ID to be used after skill enhancement."""

    ability_1_id: int
    ability_2_id: int
    ability_3_id: int
    ability_4_id: int

    trans_skill_id: int
    """Phase change. The skill ID of the next phase."""
    trans_condition_id: int
    trans_hit_count: int
    trans_text_label: str
    trans_time: float
    trans_action_id: int

    max_use_count: int
    """Currently only used on Mars (Dragon)."""
    mode_change_skill_id: int
    """Currently only used on Mega Man."""
    as_helper_skill_id: int
    """Currently only used on Mega Man (S2)."""

    is_affected_by_tension_lv1: bool
    is_affected_by_tension_lv2: bool
    is_affected_by_tension_lv3: bool
    is_affected_by_tension_lv4: bool

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "SkillDataEntry":
        return SkillDataEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            skill_type_id=data["_SkillType"],
            icon_lv1_label=data["_SkillLv1IconName"],
            icon_lv2_label=data["_SkillLv2IconName"],
            icon_lv3_label=data["_SkillLv3IconName"],
            icon_lv4_label=data["_SkillLv4IconName"],
            description_lv1_label=data["_Description1"],
            description_lv2_label=data["_Description2"],
            description_lv3_label=data["_Description3"],
            description_lv4_label=data["_Description4"],
            sp_lv1=data["_Sp"],
            sp_lv2=data["_SpLv2"],
            sp_lv3=data["_SpLv3"],
            sp_lv4=data["_SpLv4"],
            sp_ss_lv1=data["_SpEdit"],
            sp_ss_lv2=data["_SpLv2Edit"],
            sp_ss_lv3=data["_SpLv3Edit"],
            sp_ss_lv4=data["_SpLv4Edit"],
            sp_dragon_lv1=data["_SpDragon"],
            sp_dragon_lv2=data["_SpLv2Dragon"],
            sp_dragon_lv3=data["_SpLv3Dragon"],
            sp_dragon_lv4=data["_SpLv4Dragon"],
            sp_gauge_count=data["_SpGaugeCount"],
            required_buff_id=data["_RequiredBuffId"],
            required_buff_count=data["_RequiredBuffCount"],
            action_1_id=data["_ActionId1"],
            action_2_id=data["_ActionId2"],
            action_3_id=data["_ActionId3"],
            action_4_id=data["_ActionId4"],
            adv_skill_lv1=data["_AdvancedSkillLv1"],
            adv_skill_lv1_action_id=data["_AdvancedActionId1"],
            ability_1_id=data["_Ability1"],
            ability_2_id=data["_Ability2"],
            ability_3_id=data["_Ability3"],
            ability_4_id=data["_Ability4"],
            trans_skill_id=data["_TransSkill"],
            trans_condition_id=data["_TransCondition"],
            trans_hit_count=data["_TransHitCount"],
            trans_text_label=data["_TransText"],
            trans_time=data["_TransTime"],
            trans_action_id=data["_TransBuff"],
            max_use_count=data["_MaxUseNum"],
            mode_change_skill_id=data["_ModeChange"],
            as_helper_skill_id=data["_Support"],
            is_affected_by_tension_lv1=bool(data["_IsAffectedByTension"]),
            is_affected_by_tension_lv2=bool(data["_IsAffectedByTensionLv2"]),
            is_affected_by_tension_lv3=bool(data["_IsAffectedByTensionLv3"]),
            is_affected_by_tension_lv4=bool(data["_IsAffectedByTensionLv4"]),
        )

    @property
    def action_id_1_by_level(self) -> list[int]:
        """
        Get the 1st (main) action IDs for each level.

        Note that the action ID for skill lv. 1 will be located at index 0.
        """
        return [
            self.adv_skill_lv1_action_id
            if self.adv_skill_lv1_action_id and level + 1 >= self.adv_skill_lv1
            else self.action_1_id
            for level in range(SKILL_MAX_LEVEL)
        ]

    @property
    def is_attacking_skill(self) -> bool:
        """
        Check if the skill is an attacking skill.

        Currently, ``is_affected_by_tension_lv1`` is used to perform the check.
        """
        return self.is_affected_by_tension_lv1

    @property
    def has_helper_variant(self) -> bool:
        """Check if the skill will be different if used as helper skill."""
        return self.as_helper_skill_id != 0


class SkillDataAsset(MasterAssetBase):
    """Skill data asset class."""

    asset_file_name = "SkillData.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(SkillDataParser, file_path, asset_dir=asset_dir)


class SkillDataParser(MasterParserBase):
    """Class to parse the skill data."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, SkillDataEntry]:
        entries = cls.get_entries(file_path)

        return {key: SkillDataEntry.parse_raw(value) for key, value in entries.items()}
