"""Classes for handling the character data asset."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING, TextIO, Union

from dlparse.enums import Element, Language, SkillNumber, Weapon
from dlparse.errors import InvalidSkillNumError, TextLabelNotFoundError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from dlparse.mono.asset.extension import NamedEntry, SkillDiscoverableEntry, VariedEntry
from .dragon_data import DRAGON_SKILL_MAX_LEVEL
from .skill_data import CHARA_SKILL_MAX_LEVEL
from .text_label import TextAssetMultilingual

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("CharaDataEntry", "CharaDataAsset")


@dataclass
class CharaDataEntry(NamedEntry, VariedEntry, SkillDiscoverableEntry, MasterEntryBase):
    """Single entry of a character data."""

    # pylint: disable=too-many-public-methods

    # region Attributes
    weapon: Weapon
    rarity: int

    max_limit_break_count: int

    element_id: int

    chara_type_id: int

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

    mode_change_type: int
    mode_1_id: int
    mode_2_id: int
    mode_3_id: int
    mode_4_id: int
    keep_mode_on_revive: bool

    combo_original_id: int
    combo_mode_1_id: int
    combo_mode_2_id: int

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
    ss_skill_num: SkillNumber
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

    unique_dragon_inherit_skill_lv: int

    is_dragon_drive: bool
    """Bellina, etc."""
    is_playable: bool

    unique_weapon_id: int

    win_face_eye_id: int
    win_face_mouth_id: int

    max_friendship_point: int
    """Raid event units."""

    grow_material_start: Optional[datetime]
    grow_material_end: Optional[datetime]
    grow_material_id: int

    # endregion

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
    def has_mode_change(self) -> bool:
        return self.mode_change_type != 0

    @property
    def mode_ids(self) -> list[int]:
        """
        Get a list of effective mode IDs.

        This could include but not limited to:

        - Enhance mode (Bellina)

        - Buff stacks (Catherine)
        """
        return [mode_id for mode_id in (self.mode_1_id, self.mode_2_id, self.mode_3_id, self.mode_4_id) if mode_id]

    @property
    def icon_name(self) -> str:
        """Get the name of the character icon, excluding the file extension."""
        return f"{self.base_id}_{self.variation_id:02}_r{self.rarity:02}"

    @property
    def element(self) -> Element:
        """Get the element of the character."""
        return Element(self.element_id)

    @property
    def has_unique_weapon(self) -> bool:
        """Check if the character has an unique weapon."""
        return self.unique_weapon_id != 0

    @property
    def has_special_win_face(self) -> bool:
        """Check if the character has a special winning face."""
        return self.win_face_eye_id != 0 or self.win_face_mouth_id

    @property
    def ability_ids_at_max_level(self) -> list[int]:
        """Get the ability IDs at its max level."""
        ret: list[int] = []

        # DON'T use `self.is_70_mc` because some ability will not have a level increase even if it's 70 MC

        for abid in (self.ability_1_lv_4_id, self.ability_1_lv_3_id, self.ability_1_lv_2_id, self.ability_1_lv_1_id):
            if not abid:  # Ability ineffective, continue
                continue

            ret.append(abid)  # Found 1 effective ability, add it and terminate the loop
            break

        for abid in (self.ability_2_lv_4_id, self.ability_2_lv_3_id, self.ability_2_lv_2_id, self.ability_2_lv_1_id):
            if not abid:  # Ability ineffective, continue
                continue

            ret.append(abid)  # Found 1 effective ability, add it and terminate the loop
            break

        for abid in (self.ability_3_lv_4_id, self.ability_3_lv_3_id, self.ability_3_lv_2_id, self.ability_3_lv_1_id):
            if not abid:  # Ability ineffective, continue
                continue

            ret.append(abid)  # Found 1 effective ability, add it and terminate the loop
            break

        return ret

    @property
    def ability_ids_all_level(self) -> list[int]:
        return [
            ability_id for ability_id in (
                self.ability_1_lv_1_id, self.ability_1_lv_2_id, self.ability_1_lv_3_id, self.ability_1_lv_4_id,
                self.ability_2_lv_1_id, self.ability_2_lv_2_id, self.ability_2_lv_3_id, self.ability_2_lv_4_id,
                self.ability_3_lv_1_id, self.ability_3_lv_2_id, self.ability_3_lv_3_id, self.ability_3_lv_4_id,
            ) if ability_id
        ]

    @property
    def ex_ids(self) -> list[int]:
        """Get all EX ability IDs of the character ordered by the level."""
        return [self.ex_1_id, self.ex_2_id, self.ex_3_id, self.ex_4_id, self.ex_5_id]

    @property
    def ex_id_at_max_level(self) -> int:
        """Get the ID of the EX ability at the max level."""
        return self.ex_ids[-1]

    @property
    def cex_ids(self) -> list[int]:
        """Get all chained EX ability IDs of the character ordered by the level."""
        return [self.cex_1_id, self.cex_2_id, self.cex_3_id, self.cex_4_id, self.cex_5_id]

    @property
    def cex_id_at_max_level(self) -> int:
        """Get the ID of the chained EX ability at the max level."""
        return self.cex_ids[-1]

    @property
    def name_labels(self) -> list[str]:
        """
        Get a list of name labels to be used for getting the character name.

        Note that the first one should be used first to get the character name. The order matters.
        """
        return [self.name_label_2, self.name_label]

    def max_skill_level(self, skill_num: SkillNumber):
        if skill_num == SkillNumber.ABILITY:
            return CHARA_SKILL_MAX_LEVEL  # No explicit skill index info found, using the max possible level

        if skill_num.is_dragon_skill:
            if not self.unique_dragon_inherit_skill_lv:
                return DRAGON_SKILL_MAX_LEVEL

            if skill_num == SkillNumber.S1_DRAGON:
                skill_num = SkillNumber.S1
            elif skill_num == SkillNumber.S2_DRAGON:
                skill_num = SkillNumber.S2

        if skill_num == SkillNumber.S1:
            return 4 if self.is_70_mc else 3

        if skill_num == SkillNumber.S2:
            return 3 if self.is_70_mc else 2

        raise InvalidSkillNumError(skill_num)

    def get_chara_name(self, text_asset: TextAssetMultilingual, language: Language = Language.JP) -> str:
        """Get the name of the character."""
        try:
            return text_asset.get_text(language.value, self.name_label_2)
        except TextLabelNotFoundError:
            return text_asset.get_text(language.value, self.name_label)

    @classmethod
    def parse_raw(cls, data: dict[str, Union[str, int, float]]) -> "CharaDataEntry":
        return CharaDataEntry(
            id=data["_Id"],
            name_label=data["_Name"],
            name_label_2=data["_SecondName"],
            emblem_id=data["_EmblemId"],
            weapon=Weapon(data["_WeaponType"]),
            rarity=data["_Rarity"],
            max_limit_break_count=data["_MaxLimitBreakCount"],
            element_id=data["_ElementalType"],
            chara_type_id=data["_CharaType"],
            base_id=data["_BaseId"],
            variation_id=data["_VariationId"],
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
            mode_change_type=data["_ModeChangeType"],
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
            ss_skill_num=SkillNumber.s1_s2_only(data["_EditSkillLevelNum"]),
            ss_skill_cost=data["_EditSkillCost"],
            ss_skill_relation_id=data["_EditSkillRelationId"],
            ss_release_item_id=data["_EditReleaseEntityId1"],
            ss_release_item_quantity=data["_EditReleaseEntityQuantity1"],
            win_face_eye_id=data["_WinFaceEyeMotion"],
            win_face_mouth_id=data["_WinFaceEyeMotion"],
            unique_weapon_id=data["_UniqueWeaponId"],
            unique_dragon_id=data["_UniqueDragonId"],
            unique_dragon_inherit_skill_lv=bool(data["_IsConvertDragonSkillLevel"]),
            is_dragon_drive=bool(data["_WinFaceMouthMotion"]),
            is_playable=bool(data["_IsPlayable"]),
            max_friendship_point=data["_MaxFriendshipPoint"],
            grow_material_start=cls.parse_datetime(data["_GrowMaterialOnlyStartDate"]),
            grow_material_end=cls.parse_datetime(data["_GrowMaterialOnlyEndDate"]),
            grow_material_id=data["_GrowMaterialId"],
        )


class CharaDataAsset(MasterAssetBase[CharaDataEntry]):
    """Character data asset class."""

    asset_file_name = "CharaData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(CharaDataParser, file_location, asset_dir=asset_dir, file_like=file_like)

        # Cache for getting the chara data by skill ID
        self._cache_skill_id: dict[int, CharaDataEntry] = {}  # K = skill ID
        self._traversed_chara_id: set[int] = set()

    def get_chara_data_by_skill_id(
            self, asset_manager: "AssetManager", skill_id: int, /,
            playable_only: bool = True
    ) -> Optional[CharaDataEntry]:
        """
        Get the character data whose any of the skill is ``skill_id``.

        Returns ``None`` if none of the character data has a skill of ``skill_id``.
        """
        # Get the corresponding chara data from the cache, if exists
        if skill_id in self._cache_skill_id:
            return self._cache_skill_id[skill_id]

        # Traverse all un-traversed chara data
        # - Traversed results will be stored in the cache
        chara_data: CharaDataEntry
        for chara_data in filter(lambda data: data.id not in self._traversed_chara_id, self):
            # Record that the chara data has been traversed
            self._traversed_chara_id.add(chara_data.id)

            # Don't continue if ``playable_only`` and the character is not playable
            if playable_only and not chara_data.is_playable:
                continue

            # Get the skill ID entries
            entries = chara_data.get_skill_id_entries(asset_manager, include_base_if_mode=True)

            # Store each result to the cache
            for entry in entries:
                self._cache_skill_id[entry.skill_id] = chara_data

            # Return if the data is stored in the cache (found in the previous code)
            if skill_id in self._cache_skill_id:
                return self._cache_skill_id[skill_id]

        # Chara data not found, returns ``None``
        return None

    @property
    def playable_chara_data(self) -> list[CharaDataEntry]:
        """Get all character data of the playable characters."""
        return [data for data in self if data.is_playable]


class CharaDataParser(MasterParserBase[CharaDataEntry]):
    """Class to parse the character data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, CharaDataEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: CharaDataEntry.parse_raw(value) for key, value in entries.items()}
