"""Classes for handling the skill data asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("SkillIdEntry", "SkillDataEntry", "SkillDataAsset", "SkillDataParser")

SKILL_MAX_LEVEL = 4


@dataclass
class SkillIdEntry:
    """Class for a skill ID entry."""

    skill_id: int
    """Skill ID."""
    skill_num: int
    """Number of the skill. ``1`` for S1; ``2`` for S2."""
    skill_identifier: str
    """Skill identifier. This is not unique. The purpose of this is for easier skill identification."""


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

    ability_lv1_id: int
    ability_lv2_id: int
    ability_lv3_id: int
    ability_lv4_id: int

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
    """If the skill will be affected by energizing at Lv.1."""
    is_affected_by_tension_lv2: bool
    """If the skill will be affected by energizing at Lv.2."""
    is_affected_by_tension_lv3: bool
    """If the skill will be affected by energizing at Lv.3."""
    is_affected_by_tension_lv4: bool
    """If the skill will be affected by energizing at Lv.4."""

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
            ability_lv1_id=data["_Ability1"],
            ability_lv2_id=data["_Ability2"],
            ability_lv3_id=data["_Ability3"],
            ability_lv4_id=data["_Ability4"],
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
    def ability_id_by_level(self) -> list[int]:
        """
        Get the ability ID list for each level. If the ability is not applicable at the certain level, returns 0.

        Note that the ability ID for skill lv. 1 will be located at index 0.
        """
        return [self.ability_lv1_id, self.ability_lv2_id, self.ability_lv3_id, self.ability_lv4_id]

    @property
    def has_helper_variant(self) -> bool:
        """Check if the skill will be different if used as helper skill."""
        return self.as_helper_skill_id != 0

    @property
    def has_phase_changing(self) -> bool:
        """Check if the skill has phase changing available."""
        return self.trans_skill_id != 0

    def get_phase_changed_skills(self, skill_asset: "SkillDataAsset", skill_num: int) -> \
            list[SkillIdEntry]:
        """Get a list of skills of all possible transitioned skills, excluding the source skill."""
        ret: list[SkillIdEntry] = []
        added_skill_id: set[int] = set()
        current_source: SkillDataEntry = self

        if not self.has_phase_changing:
            return ret

        while trans_skill_data := skill_asset.get_data_by_id(current_source.trans_skill_id):
            if trans_skill_data.id == self.id:
                break  # Changed to source skill data

            if trans_skill_data.id in added_skill_id:
                break  # Phase looped back

            phase_num = len(ret) + 2

            ret.append(SkillIdEntry(
                trans_skill_data.id,
                skill_num,
                f"S{skill_num} P{phase_num}"
            ))
            added_skill_id.add(trans_skill_data.id)

            current_source = trans_skill_data

        return ret


class SkillDataAsset(MasterAssetBase[SkillDataEntry]):
    """Skill data asset class."""

    asset_file_name = "SkillData.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(SkillDataParser, file_path, asset_dir=asset_dir)


class SkillDataParser(MasterParserBase[SkillDataEntry]):
    """Class to parse the skill data."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, SkillDataEntry]:
        entries = cls.get_entries(file_path)

        return {key: SkillDataEntry.parse_raw(value) for key, value in entries.items()}
