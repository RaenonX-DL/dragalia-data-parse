"""Classes for handling the character data asset."""
from dataclasses import dataclass
from datetime import datetime
from typing import Union, Optional

from dlparse.enums import Element
from dlparse.errors import TextLabelNotFoundError
from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase
from .chara_mode_data import CharaModeAsset
from .skill_data import SkillDataEntry, SkillDataAsset
from .text_label import TextAsset

__all__ = ("SkillIdEntry", "CharaDataEntry", "CharaDataAsset", "CharaDataParser")


@dataclass
class SkillIdEntry:
    """Class for a skill ID entry."""

    skill_id: int
    """Skill."""
    skill_identifier: str
    """Skill identifier. This is not unique. The purpose of this is for easier skill identification."""
    skill_unique_id: str
    """A unique ID for identifying the skill. The purpose of this is for indexing at the website."""


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

    # region Passives
    passive_1_lv_1_id: int
    passive_1_lv_2_id: int
    passive_1_lv_3_id: int
    passive_1_lv_4_id: int
    passive_2_lv_1_id: int
    passive_2_lv_2_id: int
    passive_2_lv_3_id: int
    passive_2_lv_4_id: int
    passive_3_lv_1_id: int
    passive_3_lv_2_id: int
    passive_3_lv_3_id: int
    passive_3_lv_4_id: int
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
    ss_skill_level: int
    ss_skill_cost: int
    ss_skill_relation_id: int
    """SS cost offset or similar. OG!Hawk and OG!Nefaria for now."""
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

    def get_skill_identifiers(self, chara_mode_asset: CharaModeAsset, /,
                              text_asset: Optional[TextAsset] = None,
                              skill_asset: Optional[SkillDataAsset] = None) \
            -> list[SkillIdEntry]:
        """
        Get the skill ID entries of a character.

        This includes different skills in different modes, helper variants, and phase changed IDs, if any.

        If ``text_asset`` is not provided, mode name (if any) will not be able to convert to text.

        If ``skill_asset`` is not provided, support skill variant (if any) and the phase changing variant (if any)
        will not be included.

        The identifier is not the name of the skill. Instead, it's a name commonly used in between players.
        For skill 1, the identifier will be ``S1``, etc.

        The main purpose of unique

        For skills that comes from a mode, the name of the mode will be appended at the end of the identifier.
        For example, the identifier of Bellina's S2 in enhanced mode will be ``S2 (不羈伴侶)``.
        """
        ret: list[SkillIdEntry] = [
            SkillIdEntry(self.skill_1_id, "S1", "S1/BASE"),
            SkillIdEntry(self.skill_2_id, "S2", "S2/BASE")
        ]

        # Attach skill IDs in different mode from mode asset
        for mode_id in self.mode_ids:
            if mode_data := chara_mode_asset.get_data_by_id(mode_id):
                mode_name = f"Mode #{mode_id}"
                if text_asset:
                    mode_name = text_asset.to_text(mode_data.text_label) or mode_name

                if model_skill_1_id := mode_data.skill_id_1:
                    ret.append(SkillIdEntry(model_skill_1_id, f"S1 ({mode_name})", f"S1/{mode_data.id}"))

                if model_skill_2_id := mode_data.skill_id_2:
                    ret.append(SkillIdEntry(model_skill_2_id, f"S2 ({mode_name})", f"S2/{mode_data.id}"))

        if skill_asset:
            skill_1_data: SkillDataEntry = skill_asset.get_data_by_id(self.skill_1_id)
            skill_2_data: SkillDataEntry = skill_asset.get_data_by_id(self.skill_2_id)

            # Attach helper skill variant if given (currently only S1 will be used as helper skill)
            if skill_1_data and skill_1_data.has_helper_variant:
                ret.append(SkillIdEntry(
                    skill_1_data.as_helper_skill_id,
                    text_asset.to_text("SKILL_IDENTIFIER_HELPER") if text_asset else "Helper",
                    "S1/HELPER"
                ))

            if skill_1_data and skill_1_data.has_phase_changing:
                ret.extend(self._get_phase_skill_ids(skill_1_data, skill_asset, 1))

            if skill_2_data and skill_2_data.has_phase_changing:
                ret.extend(self._get_phase_skill_ids(skill_2_data, skill_asset, 2))

        return ret

    def _get_phase_skill_ids(self, source_skill_data: SkillDataEntry, skill_asset: SkillDataAsset, skill_num: int) -> \
            list[SkillIdEntry]:
        """Get a list of skills containing skills in all possible phases."""
        ret: list[SkillIdEntry] = []
        added_skill_id: set[int] = set()
        current_source: SkillDataEntry = source_skill_data

        if not source_skill_data.has_phase_changing:
            return ret

        while trans_skill_data := skill_asset.get_data_by_id(current_source.trans_skill_id):
            if trans_skill_data.id == source_skill_data.id:
                break  # Changed to source skill data

            if trans_skill_data.id in added_skill_id:
                break  # Phase looped back

            phase_num = len(ret) + 2

            ret.append(SkillIdEntry(
                trans_skill_data.id,
                f"S{skill_num} P{phase_num}",
                f"S{skill_num}/P{phase_num}"
            ))
            added_skill_id.add(trans_skill_data.id)

            current_source = trans_skill_data

        return ret

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
            passive_1_lv_1_id=data["_Abilities11"],
            passive_1_lv_2_id=data["_Abilities12"],
            passive_1_lv_3_id=data["_Abilities13"],
            passive_1_lv_4_id=data["_Abilities14"],
            passive_2_lv_1_id=data["_Abilities21"],
            passive_2_lv_2_id=data["_Abilities22"],
            passive_2_lv_3_id=data["_Abilities23"],
            passive_2_lv_4_id=data["_Abilities24"],
            passive_3_lv_1_id=data["_Abilities31"],
            passive_3_lv_2_id=data["_Abilities32"],
            passive_3_lv_3_id=data["_Abilities33"],
            passive_3_lv_4_id=data["_Abilities34"],
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
            ss_skill_level=data["_EditSkillLevelNum"],
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

    def get_all_skill_ids(self, chara_mode_asset: CharaModeAsset, /,
                          skill_asset: Optional[SkillDataAsset] = None) -> list[int]:
        """
        Get all skill IDs of all characters.

        If ``skill_asset`` is not provided, skills that has helper variant will not be included.
        """
        ret: list[int] = []

        for chara_data in self:
            skill_ids = [skill_id_entry.skill_id for skill_id_entry
                         in chara_data.get_skill_identifiers(chara_mode_asset, skill_asset=skill_asset)]
            ret.extend(skill_ids)

        return ret


class CharaDataParser(MasterParserBase[CharaDataEntry]):
    """Class to parse the character data file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, CharaDataEntry]:
        entries = cls.get_entries(file_path)

        return {key: CharaDataEntry.parse_raw(value) for key, value in entries.items()}
