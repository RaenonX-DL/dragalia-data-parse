"""Classes for handling the character data asset."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Union

from dlparse.enums import Element
from dlparse.errors import ActionDataNotFoundError, InvalidSkillNumError, TextLabelNotFoundError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from .ability import AbilityEntry
from .skill_data import SkillDataEntry, SkillIdEntry, SkillIdentifierLabel
from .text_label import TextAsset

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("CharaDataEntry", "CharaDataAsset", "CharaDataParser")


@dataclass
class CharaDataEntry(MasterEntryBase):
    """Single entry of a character data."""

    name_label: str
    second_name_label: str
    emblem_id: int

    weapon_type_id: int
    rarity: int

    max_limit_break_count: int

    element_id: int

    chara_type_id: int
    chara_base_id: int
    chara_variation_id: int

    # region Parameters
    max_hp: int
    max_hp_1: int
    plus_hp_0: int
    plus_hp_1: int
    plus_hp_2: int
    plus_hp_3: int
    plus_hp_4: int
    plus_hp_5: int
    mc_full_bonus_hp: int

    max_atk: int
    max_atk_1: int
    plus_atk_0: int
    plus_atk_1: int
    plus_atk_2: int
    plus_atk_3: int
    plus_atk_4: int
    plus_atk_5: int
    mc_full_bonus_atk: int

    def_coef: float
    # endregion

    mode_change_id: int
    """Gala Leif / Mitsuba, etc."""
    mode_1_id: int
    mode_2_id: int
    mode_3_id: int
    mode_4_id: int
    keep_mode_on_revive: bool

    combo_original_id: int
    combo_mode_1_id: int
    combo_mode_2_id: int

    skill_1_id: int
    skill_2_id: int

    # region Passive ability
    ability_1_lv_1_id: int
    ability_1_lv_2_id: int
    ability_1_lv_3_id: int
    ability_1_lv_4_id: int
    ability_2_lv_1_id: int
    ability_2_lv_2_id: int
    ability_2_lv_3_id: int
    ability_2_lv_4_id: int
    ability_3_lv_1_id: int
    ability_3_lv_2_id: int
    ability_3_lv_3_id: int
    ability_3_lv_4_id: int
    # endregion

    # region EX
    ex_1_id: int
    ex_2_id: int
    ex_3_id: int
    ex_4_id: int
    ex_5_id: int

    cex_1_id: int
    cex_2_id: int
    cex_3_id: int
    cex_4_id: int
    cex_5_id: int
    # endregion

    fs_type_id: int
    fs_count_max: int

    # region Shared Skills
    ss_cost_max_self: int
    ss_skill_id: int
    ss_skill_num: int
    """
    Corresponding skill num. If the shared skill corresponds to S1, this will be ``1``.

    ``0`` if the character does not have a sharable skill.
    """
    ss_skill_cost: int
    ss_skill_relation_id: int
    """SS cost offset or similar. OG!Hawk and OG!Nefaria has this for now."""
    ss_release_item_id: int
    ss_release_item_quantity: int
    # endregion

    unique_dragon_id: int

    is_dragon_drive: bool
    """Bellina, etc."""
    is_playable: bool

    max_friendship_point: int
    """Raid event units."""

    grow_material_start: Optional[datetime]
    grow_material_end: Optional[datetime]
    grow_material_id: int

    @property
    def is_70_mc(self) -> bool:
        """Check if the character has mana spiral."""
        return self.max_limit_break_count >= 5

    @property
    def max_hp_at_50(self) -> int:
        """
        Get the max HP of the character at 50 MC.

        This includes the max base parameters,
        with the bonus given from mana circle and the additional bonus after 50 MC.
        """
        base = self.max_hp
        mc_plus = self.plus_hp_0 + self.plus_hp_1 + self.plus_hp_2 + self.plus_hp_3 + self.plus_hp_4
        full_bonus = self.mc_full_bonus_hp

        return base + mc_plus + full_bonus

    @property
    def max_hp_at_70(self) -> int:
        """
        Get the max HP of the character at 70 MC.

        This includes the max base parameters,
        with the bonus given from mana circle and the additional bonus after 50 MC.
        """
        base = self.max_hp_1
        mc_plus = self.plus_hp_0 + self.plus_hp_1 + self.plus_hp_2 + self.plus_hp_3 + self.plus_hp_4 + self.plus_hp_5
        full_bonus = self.mc_full_bonus_hp

        return base + mc_plus + full_bonus

    @property
    def max_hp_current(self) -> int:
        """
        Get the max HP of the character at the current maximum max MC.

        This includes the max base parameters,
        with the bonus given from mana circle and the additional bonus after 50 MC.
        """
        if self.is_70_mc:
            return self.max_hp_at_70

        return self.max_hp_at_50

    @property
    def max_atk_at_50(self) -> int:
        """
        Get the max ATK of the character at 50 MC.

        This includes the max base parameters,
        with the bonus given from mana circle and the additional bonus after 50 MC.
        """
        base = self.max_atk
        mc_plus = self.plus_atk_0 + self.plus_atk_1 + self.plus_atk_2 + self.plus_atk_3 + self.plus_atk_4
        full_bonus = self.mc_full_bonus_atk

        return base + mc_plus + full_bonus

    @property
    def max_atk_at_70(self) -> int:
        """
        Get the max ATK of the character at 70 MC.

        This includes the max base parameters,
        with the bonus given from mana circle and the additional bonus after 50 MC.
        """
        base = self.max_atk_1
        mc_plus = sum((
            self.plus_atk_0, self.plus_atk_1, self.plus_atk_2,
            self.plus_atk_3, self.plus_atk_4, self.plus_atk_5
        ))
        full_bonus = self.mc_full_bonus_atk

        return base + mc_plus + full_bonus

    @property
    def max_atk_current(self) -> int:
        """
        Get the max ATK of the character at the current maximum max MC.

        This includes the max base parameters,
        with the bonus given from mana circle and the additional bonus after 50 MC.
        """
        if self.is_70_mc:
            return self.max_atk_at_70

        return self.max_atk_at_50

    @property
    def mode_ids(self) -> list[int]:
        """
        Get a list of effective mode IDs.

        This could include but not limited to:

        - Enhance mode (Bellina)

        - Buff stacks (Catherine)
        """
        return [mode_id for mode_id in (self.mode_1_id, self.mode_2_id, self.mode_3_id, self.mode_4_id)
                if mode_id != 0]

    @property
    def custom_id(self) -> str:
        """
        Custom ID of the character.

        This ID will be in the format of ``{CHARA_BASE_ID}/{VARIATION_ID}``.
        """
        return f"{self.chara_base_id}/{self.chara_variation_id}"

    @property
    def element(self) -> Element:
        """Get the element of the character."""
        return Element(self.element_id)

    @property
    def ability_ids_all_level(self) -> list[int]:
        """Get a list of effective (non-zero) ability / passive IDs at all levels."""
        return [
            ability_id for ability_id in (
                self.ability_1_lv_1_id, self.ability_1_lv_2_id, self.ability_1_lv_3_id, self.ability_1_lv_4_id,
                self.ability_2_lv_1_id, self.ability_2_lv_2_id, self.ability_2_lv_3_id, self.ability_2_lv_4_id,
                self.ability_3_lv_1_id, self.ability_3_lv_2_id, self.ability_3_lv_3_id, self.ability_3_lv_4_id,
            ) if ability_id
        ]

    def max_skill_level(self, skill_num: int):
        """
        Get the maximum skill level of a skill.

        To get the max level of S1, set ``skill_num`` to ``1``.

        :raises InvalidSkillNumError: if `skill_num` is invalid
        """
        if skill_num == 1:  # S1
            return 4 if self.is_70_mc else 3

        if skill_num == 2:  # S2
            return 3 if self.is_70_mc else 2

        raise InvalidSkillNumError(skill_num)

    def _skill_id_base(self) -> list[SkillIdEntry]:
        ret: list[SkillIdEntry] = [
            SkillIdEntry(self.skill_1_id, 1, SkillIdentifierLabel.S1_BASE),
            SkillIdEntry(self.skill_2_id, 2, SkillIdentifierLabel.S2_BASE)
        ]

        if self.ss_skill_id:
            ret.append(SkillIdEntry(self.ss_skill_id, self.ss_skill_num, SkillIdentifierLabel.SHARED))

        return ret

    def _skill_id_mode(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        ret: list[SkillIdEntry] = []

        for mode_id in self.mode_ids:
            if mode_data := asset_manager.asset_chara_mode.get_data_by_id(mode_id):
                if model_skill_1_id := mode_data.skill_id_1:
                    ret.append(SkillIdEntry(model_skill_1_id, 1, SkillIdentifierLabel.of_mode(1, mode_id)))

                if model_skill_2_id := mode_data.skill_id_2:
                    ret.append(SkillIdEntry(model_skill_2_id, 2, SkillIdentifierLabel.of_mode(2, mode_id)))

        return ret

    def _skill_id_hit_labels(
            self, asset_manager: "AssetManager", skill_data: SkillDataEntry, skill_num: int
    ) -> dict[str, int]:
        hit_labels: dict[str, int] = {}

        # Load all hit labels of the skill
        for action_id in skill_data.action_id_1_by_level:
            for skill_lv in range(1, self.max_skill_level(skill_num) + 1):
                try:
                    prefab = asset_manager.loader_pa.get_prefab(action_id)
                    for hit_label, _ in prefab.get_hit_actions(skill_lv):
                        hit_labels[hit_label] = skill_num
                except ActionDataNotFoundError:
                    pass  # If prefab file not found, nothing should happen

        return hit_labels

    def _skill_id_action_condition_enhanced(
            self, asset_manager: "AssetManager", skill_id: int, skill_num: int, src_skill_num: int,
            hit_labels: dict[str, int], phase_counter: dict[int, int]
    ) -> SkillIdEntry:
        # Get the label to be used
        if src_skill_num == skill_num:
            # Self-enhancing, considered as phase instead
            label = SkillIdentifierLabel.of_phase(skill_num, phase_counter[skill_num])
            phase_counter[skill_num] += 1
        else:
            # Enhanced by other skill
            label = SkillIdentifierLabel.skill_enhanced_by_skill(skill_num, src_skill_num)

        # Get the other hit labels (if available) for further discovery
        skill_data = asset_manager.asset_skill.get_data_by_id(skill_id)
        hit_labels.update(self._skill_id_hit_labels(asset_manager, skill_data, skill_num))

        # Return enhanced skill ID entry
        return SkillIdEntry(skill_id, skill_num, label)

    def _skill_id_action_condition(
            self, asset_manager: "AssetManager", skill_1_data: SkillDataEntry, skill_2_data: SkillDataEntry
    ) -> list[SkillIdEntry]:
        ret: list[SkillIdEntry] = []

        # Initial hit labels to be discovered
        hit_labels = (self._skill_id_hit_labels(asset_manager, skill_1_data, 1)
                      | self._skill_id_hit_labels(asset_manager, skill_2_data, 2))
        hit_labels_searched: set[str] = set()

        # Counter to be used if the skill is self-enhancing (consider as phased skills instead)
        # Such case occurs on Xander (`10150201`)
        phase_counter = {1: 2, 2: 2}

        # Check each hit labels to see if there are any skill enhancements
        while hit_labels:
            hit_label, src_skill_num = hit_labels.popitem()

            if hit_label in hit_labels_searched:
                continue  # Hit label already searched, skipping

            hit_labels_searched.add(hit_label)

            if hit_label not in asset_manager.asset_hit_attr:
                continue  # Hit label could be missing - officials inserted dummy data

            action_cond_id = asset_manager.asset_hit_attr.get_data_by_id(hit_label).action_condition_id
            if not action_cond_id:
                continue  # Action condition ID = 0 - not used

            action_cond = asset_manager.asset_action_cond.get_data_by_id(action_cond_id)
            if not action_cond:
                continue  # Action condition data not found - officials inserted dummy action condition data

            enhance_targets = [
                (1, action_cond.enhance_skill_1_id),
                (2, action_cond.enhance_skill_2_id)
            ]

            for target_skill_num, target_skill_id in enhance_targets:
                if not target_skill_id:
                    continue  # Enhance target skill ID not set (= 0)

                ret.append(self._skill_id_action_condition_enhanced(
                    asset_manager, target_skill_id, target_skill_num, src_skill_num, hit_labels, phase_counter
                ))

        return ret

    @staticmethod
    def _skill_id_helper_variant(skill_1_data: SkillDataEntry) -> list[SkillIdEntry]:
        ret: list[SkillIdEntry] = []

        if skill_1_data and skill_1_data.has_helper_variant:
            ret.append(SkillIdEntry(
                skill_1_data.as_helper_skill_id,
                1,
                SkillIdentifierLabel.HELPER
            ))

        return ret

    @staticmethod
    def _skill_id_phase_change(
            asset_manager: "AssetManager", skill_1_data: SkillDataEntry, skill_2_data: SkillDataEntry
    ) -> list[SkillIdEntry]:
        ret: list[SkillIdEntry] = []

        if skill_1_data and skill_1_data.has_phase_changing:
            ret.extend(skill_1_data.get_phase_changed_skills(asset_manager.asset_skill, 1))

        if skill_2_data and skill_2_data.has_phase_changing:
            ret.extend(skill_2_data.get_phase_changed_skills(asset_manager.asset_skill, 2))

        return ret

    def _skill_id_from_skill_data(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        ret: list[SkillIdEntry] = []

        skill_1_data: SkillDataEntry = asset_manager.asset_skill.get_data_by_id(self.skill_1_id)
        skill_2_data: SkillDataEntry = asset_manager.asset_skill.get_data_by_id(self.skill_2_id)

        ret.extend(self._skill_id_action_condition(asset_manager, skill_1_data, skill_2_data))
        ret.extend(self._skill_id_helper_variant(skill_1_data))
        ret.extend(self._skill_id_phase_change(asset_manager, skill_1_data, skill_2_data))

        return ret

    def _skill_id_from_ability_data(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        ret: list[SkillIdEntry] = []

        ability_ids_to_search: list[int] = self.ability_ids_all_level
        while ability_ids_to_search:
            ability_id: int = ability_ids_to_search.pop(0)

            # Get the ability data
            ability_data: AbilityEntry = asset_manager.asset_ability_data.get_data_by_id(ability_id)

            # Add all other ability IDs to be searched
            ability_ids_to_search.extend(ability_data.other_ability_ids)

            # Add skill IDs enhanced by the ability
            for skill_id, skill_num in ability_data.enhanced_skills:
                ret.append(SkillIdEntry(skill_id, skill_num,
                                        SkillIdentifierLabel.skill_enhanced_by_ability(skill_num, ability_id)))

        return ret

    def get_skill_id_entries(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        """
        Get the skill ID entries of a character.

        This includes different skills in different modes, helper variants, and phase changed IDs, if any.

        If ``asset_text`` is not provided, mode name (if any) will not be able to convert to text.
        ``Mode #<MODE_ID>`` will be the identifier instead.

        If ``asset_skill`` is not provided, support skill variant (if any) and the phase changing variant (if any)
        will not be included.

        If any of ``loader_action``, ``asset_skill``, ``asset_hit_attr`` or ``asset_action_condition``
        are not provided, skills that can be enhanced by using another skill (if any) will not be included.
        """
        ret: list[SkillIdEntry] = self._skill_id_base()

        ret.extend(self._skill_id_mode(asset_manager))
        ret.extend(self._skill_id_from_skill_data(asset_manager))
        ret.extend(self._skill_id_from_ability_data(asset_manager))

        return SkillIdEntry.merge(ret)

    def get_chara_name(self, text_asset: TextAsset) -> str:
        """Get the name of the character."""
        try:
            return text_asset.to_text(self.second_name_label, silent_fail=False)
        except TextLabelNotFoundError:
            return text_asset.to_text(self.name_label)

    @classmethod
    def parse_raw(cls, data: dict[str, Union[str, int, float]]) -> "CharaDataEntry":
        return CharaDataEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            second_name_label=data["_SecondName"],
            emblem_id=data["_EmblemId"],
            weapon_type_id=data["_WeaponType"],
            rarity=data["_Rarity"],
            max_limit_break_count=data["_MaxLimitBreakCount"],
            element_id=data["_ElementalType"],
            chara_type_id=data["_CharaType"],
            chara_base_id=data["_BaseId"],
            chara_variation_id=data["_VariationId"],
            max_hp=data["_MaxHp"],
            max_hp_1=data["_AddMaxHp1"],
            plus_hp_0=data["_PlusHp0"],
            plus_hp_1=data["_PlusHp1"],
            plus_hp_2=data["_PlusHp2"],
            plus_hp_3=data["_PlusHp3"],
            plus_hp_4=data["_PlusHp4"],
            plus_hp_5=data["_PlusHp5"],
            mc_full_bonus_hp=data["_McFullBonusHp5"],
            max_atk=data["_MaxAtk"],
            max_atk_1=data["_AddMaxAtk1"],
            plus_atk_0=data["_PlusAtk0"],
            plus_atk_1=data["_PlusAtk1"],
            plus_atk_2=data["_PlusAtk2"],
            plus_atk_3=data["_PlusAtk3"],
            plus_atk_4=data["_PlusAtk4"],
            plus_atk_5=data["_PlusAtk5"],
            mc_full_bonus_atk=data["_McFullBonusAtk5"],
            def_coef=data["_DefCoef"],
            mode_change_id=data["_ModeChangeType"],
            mode_1_id=data["_ModeId1"],
            mode_2_id=data["_ModeId2"],
            mode_3_id=data["_ModeId3"],
            mode_4_id=data["_ModeId4"],
            keep_mode_on_revive=bool(data["_KeepModeOnRevive"]),
            combo_original_id=data["_OriginCombo"],
            combo_mode_1_id=data["_Mode1Combo"],
            combo_mode_2_id=data["_Mode2Combo"],
            skill_1_id=data["_Skill1"],
            skill_2_id=data["_Skill2"],
            ability_1_lv_1_id=data["_Abilities11"],
            ability_1_lv_2_id=data["_Abilities12"],
            ability_1_lv_3_id=data["_Abilities13"],
            ability_1_lv_4_id=data["_Abilities14"],
            ability_2_lv_1_id=data["_Abilities21"],
            ability_2_lv_2_id=data["_Abilities22"],
            ability_2_lv_3_id=data["_Abilities23"],
            ability_2_lv_4_id=data["_Abilities24"],
            ability_3_lv_1_id=data["_Abilities31"],
            ability_3_lv_2_id=data["_Abilities32"],
            ability_3_lv_3_id=data["_Abilities33"],
            ability_3_lv_4_id=data["_Abilities34"],
            ex_1_id=data["_ExAbilityData1"],
            ex_2_id=data["_ExAbilityData2"],
            ex_3_id=data["_ExAbilityData3"],
            ex_4_id=data["_ExAbilityData4"],
            ex_5_id=data["_ExAbilityData5"],
            cex_1_id=data["_ExAbility2Data1"],
            cex_2_id=data["_ExAbility2Data2"],
            cex_3_id=data["_ExAbility2Data3"],
            cex_4_id=data["_ExAbility2Data4"],
            cex_5_id=data["_ExAbility2Data5"],
            fs_type_id=data["_ChargeType"],
            fs_count_max=data["_MaxChargeLv"],
            ss_cost_max_self=data["_HoldEditSkillCost"],
            ss_skill_id=data["_EditSkillId"],
            ss_skill_num=data["_EditSkillLevelNum"],
            ss_skill_cost=data["_EditSkillCost"],
            ss_skill_relation_id=data["_EditSkillRelationId"],
            ss_release_item_id=data["_EditReleaseEntityId1"],
            ss_release_item_quantity=data["_EditReleaseEntityQuantity1"],
            unique_dragon_id=data["_UniqueDragonId"],
            is_dragon_drive=bool(data["_IsEnhanceChara"]),
            is_playable=bool(data["_IsPlayable"]),
            max_friendship_point=data["_MaxFriendshipPoint"],
            grow_material_start=cls.parse_datetime(data["_GrowMaterialOnlyStartDate"]),
            grow_material_end=cls.parse_datetime(data["_GrowMaterialOnlyEndDate"]),
            grow_material_id=data["_GrowMaterialId"],
        )


class CharaDataAsset(MasterAssetBase[CharaDataEntry]):
    """Character data asset class."""

    asset_file_name = "CharaData.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(CharaDataParser, file_path, asset_dir=asset_dir)


class CharaDataParser(MasterParserBase[CharaDataEntry]):
    """Class to parse the character data file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, CharaDataEntry]:
        entries = cls.get_entries(file_path)

        return {key: CharaDataEntry.parse_raw(value) for key, value in entries.items()}
