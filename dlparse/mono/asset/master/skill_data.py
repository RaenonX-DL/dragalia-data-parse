"""Classes for handling the skill data asset."""
from collections import Counter
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, TextIO, Union

from dlparse.errors import InvalidSkillLevelError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("SkillDataEntry", "SkillDataAsset", "CHARA_SKILL_MAX_LEVEL")

CHARA_SKILL_MAX_LEVEL = 4


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

    chain_group_id: int

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

    @property
    def action_ids_set(self) -> set[int]:
        """Get a set of all possible and effective action IDs."""
        # - {0} for removing ineffective AIDs
        return {self.action_1_id, self.action_2_id, self.action_3_id, self.action_4_id,
                self.adv_skill_lv1_action_id} - {0}

    @property
    def action_ids_list(self) -> list[int]:
        """
        Get a list of effective action IDs, according to their order.

        This does **not** return the advanced (``adv_skill_lv1_action_id``) one.
        """
        return [
            action_id for action_id in [self.action_1_id, self.action_2_id, self.action_3_id, self.action_4_id]
            if action_id
        ]

    @property
    def ability_id_by_level(self) -> list[int]:
        """
        Get the ability ID list for each level. If the ability is not applicable at the certain level, return 0.

        Note that the ability ID for skill lv. 1 will be located at index 0.
        """
        return [self.ability_lv1_id, self.ability_lv2_id, self.ability_lv3_id, self.ability_lv4_id]

    @property
    def has_helper_variant(self) -> bool:
        """Check if the skill will be different if used as helper skill."""
        return self.as_helper_skill_id != 0

    @property
    def has_phase_variant(self) -> bool:
        """Check if the skill has a phase variant."""
        return self.trans_skill_id != 0

    @property
    def has_chain_variant(self) -> bool:
        """Check if the skill has a chain variant."""
        return self.chain_group_id != 0

    @property
    def action_id_count(self) -> int:
        """Get the count of action IDs available."""
        return len(self.action_ids_list)

    def get_action_id_by_level(self, max_level: int = None) -> list[tuple[int, int, float]]:
        """
        Get the action IDs, skill level and the probability by the skill level.

        The 1st element is action ID; the 2nd element is the corresponding skill level;
        the 3rd element is the probability of the action.

        Note that the skill level (2nd element) returned starts from 1, to reflect the actual skill level.
        """
        if not max_level:
            # Set ``max_level`` to max possible level if falsy (None or 0)
            max_level = CHARA_SKILL_MAX_LEVEL

        ret: list[tuple[int, int, float]] = []

        for level in range(1, max_level + 1):
            is_advanced = self.adv_skill_lv1_action_id and level >= self.adv_skill_lv1

            # Check if the skill is using the advanced action
            if is_advanced:
                ret.append((self.adv_skill_lv1_action_id, level, 1))
                continue  # Advanced skill have 100% probability only, therefore only 1 entry should be appended

            # Check the weight of the each action
            counter = Counter(self.action_ids_list)
            for action_id, appearances in counter.items():
                prob = appearances / self.action_id_count

                ret.append((action_id, level, prob))

        return ret

    def get_sp_at_level(self, level: int) -> int:
        """
        Get SP at a certain skill ``level``.

        :raises InvalidSkillLevelError: if the skill level is invalid
        """
        if level == 1:
            return self.sp_lv1
        if level == 2:
            return self.sp_lv2
        if level == 3:
            return self.sp_lv3
        if level == 4:
            return self.sp_lv4

        raise InvalidSkillLevelError(level)

    def get_sp_gradual_fill_pct_at_level(self, level: int, asset_manager: "AssetManager") -> float:
        """
        Get SP filling % per second at ``level``.

        :raises InvalidSkillLevelError: if the skill level is invalid
        """
        try:
            ability_id = self.ability_id_by_level[level - 1]
        except IndexError as ex:
            raise InvalidSkillLevelError(level) from ex

        if not ability_id:
            # No related ability
            return 0

        root_ability_data = asset_manager.asset_ability_data.get_data_by_id(ability_id)
        action_conds = [
            asset_manager.asset_action_cond.get_data_by_id(action_condition_id)
            for ability_data in root_ability_data.get_all_ability(asset_manager.asset_ability_data).values()
            for action_condition_id in ability_data.action_conditions
        ]
        return sum(action_cond.regen_sp_pct for action_cond in action_conds)

    def get_ss_sp_at_level(self, level: int) -> int:
        """
        Get SS SP at a certain skill ``level``.

        :raises InvalidSkillLevelError: if the skill level is invalid
        """
        if level == 1:
            return self.sp_ss_lv1
        if level == 2:
            return self.sp_ss_lv2
        if level == 3:
            return self.sp_ss_lv3
        if level == 4:
            return self.sp_ss_lv4

        raise InvalidSkillLevelError(level)

    def get_icon_name_at_level(self, level: int) -> str:
        """Get the skill icon name at ``level``."""
        return [self.icon_lv1_label, self.icon_lv2_label, self.icon_lv3_label, self.icon_lv4_label][level - 1]

    def get_description_label_at_level(self, level: int) -> str:
        """Get the skill description label at ``level``."""
        return [
            self.description_lv1_label,
            self.description_lv2_label,
            self.description_lv3_label,
            self.description_lv4_label
        ][level - 1]

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
            chain_group_id=data["_ChainGroupId"],
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


class SkillDataAsset(MasterAssetBase[SkillDataEntry]):
    """Skill data asset class."""

    asset_file_name = "SkillData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(SkillDataParser, file_location, asset_dir=asset_dir, file_like=file_like)


class SkillDataParser(MasterParserBase[SkillDataEntry]):
    """Class to parse the skill data."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, SkillDataEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: SkillDataEntry.parse_raw(value) for key, value in entries.items()}
