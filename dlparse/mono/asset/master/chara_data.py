"""Classes for handling the character data asset."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING, TextIO, Union

from dlparse.enums import Element, ModeChangeType, SkillNumber, UnitType, Weapon
from dlparse.errors import InvalidSkillNumError, NoUniqueDragonError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from dlparse.mono.asset.extension import SkillIdEntry, SkillIdentifierLabel, UnitAsset, UnitEntry
from .dragon_data import DRAGON_SKILL_MAX_LEVEL, DragonDataAsset, DragonDataEntry
from .skill_data import CHARA_SKILL_MAX_LEVEL

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("CharaDataEntry", "CharaDataAsset")


@dataclass
class CharaDataEntry(UnitEntry, MasterEntryBase):
    """Single entry of a character data."""

    # pylint: disable=too-many-public-methods

    # region Attributes
    weapon: Weapon

    max_limit_break_count: int

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

    mode_change_type: ModeChangeType
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
    """
    Corresponding skill num. If the shared skill corresponds to S1, this will be ``1``.

    ``0`` if the character does not have a sharable skill.
    """
    ss_skill_relation_id: int
    """SS cost offset or similar. OG!Hawk and OG!Nefaria has this for now."""
    ss_release_item_id: int
    ss_release_item_quantity: int
    # endregion

    unique_dragon_inherit_skill_lv: int

    is_dragon_drive: bool
    """Bellina, etc."""

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
        return self.mode_change_type.is_effective

    @property
    def change_on_start(self) -> bool:
        return self.mode_change_type.change_on_start

    @property
    def mode_ids(self) -> list[int]:
        """
        Get a list of effective mode IDs.

        This could include but not limited to:

        - Enhance mode (Bellina)

        - Buff stacks (Catherine)

        Note that this does not return the default mode ID, which is usually mode 1.
        For getting the mode IDs including the default one, use ``mode_ids_effective_only`` instead.
        """
        return [mode_id for mode_id in (self.mode_1_id, self.mode_2_id, self.mode_3_id, self.mode_4_id) if mode_id]

    @property
    def mode_ids_include_default(self) -> tuple[int, ...]:
        """
        Get a list of effective mode IDs, including the default one (mode 0) if available.

        Note that the default is not guaranteed to be included
        because some characters do not use their default weapon combo at all. For example, JOKER.

        The difference between this and ``mode_ids`` is that for some units with default combo like Bellina,
        her mode IDs are 0, 12, 0, 0.
        In this case, ``mode_ids`` on Bellina is ``[12]`` while calling this on Bellina returns ``[0, 12]``.

        For getting the mode IDs without the default one, use ``mode_ids`` instead.
        """
        mode_ids = (self.mode_1_id, self.mode_2_id, self.mode_3_id, self.mode_4_id)

        if mode_ids[-1]:  # All modes in-use
            return mode_ids

        for last_idx in range(2, len(mode_ids) + 1):
            if not mode_ids[-last_idx]:
                continue  # Last mode ID is not in-use, continue searching

            return mode_ids[:-last_idx + 1]  # All mode IDs including the last in-use mode

        return tuple([0])  # All mode IDs not in-use, return a tuple containing a single `0` for default mode

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
    def icon_name(self) -> str:
        return f"{self.base_id}_{self.variation_id:02}_r{self.rarity:02}"

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
    def unit_type(self) -> UnitType:
        return UnitType.CHARACTER

    @property
    def self_skill_id_entries(self) -> list[SkillIdEntry]:
        return [
            SkillIdEntry(self.skill_1_id, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
            SkillIdEntry(self.skill_2_id, SkillNumber.S2, SkillIdentifierLabel.S2_BASE)
        ]

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

    def get_dragon_data(self, dragon_asset: DragonDataAsset) -> DragonDataEntry:
        """
        Get the unique dragon data of this character.

        :raises NoUniqueDragonError: if this character does not have an unique dragon
        """
        if not self.unique_dragon_id:
            raise NoUniqueDragonError(self.id)

        return dragon_asset.get_data_by_id(self.unique_dragon_id)

    def get_normal_attack_variants(self, asset_manager: "AssetManager") -> list[tuple[int, int], ...]:
        """
        Get all normal attack variants.

        1st element of each return is the variant source mode ID;
        2nd element of each return is the normal attack root action ID.

        Variant source mode ID could have the special values below:

        - ``0`` if the corresponding variant is the default one.
        - ``-1`` if the corresponding variant comes from the unique dragon.
        """
        weapon_type_data = asset_manager.asset_weapon_type.get_data_by_weapon(self.weapon)
        default_variant_by_weapon = (0, weapon_type_data.root_normal_attack_action_id)

        ret = []

        for mode_id in self.mode_ids_include_default:
            if not mode_id:
                ret.append(default_variant_by_weapon)
                continue

            mode_data = asset_manager.asset_chara_mode.get_data_by_id(mode_id)

            # Having mode ID does not mean the mode data exists
            # - Althemia (10840401) has mode 1 as #57 but no corresponding data exists
            if not mode_data:
                continue

            unique_combo_id = mode_data.unique_combo_id
            if not unique_combo_id:
                continue  # Unique combo unavailable

            unique_combo_data = asset_manager.asset_chara_unique_combo.get_data_by_id(mode_data.unique_combo_id)

            # Having unique combo ID does not mean the unique combo exists
            # - Grace (10850503) has unique combo as #45 but no corresponding data exists
            if not unique_combo_data:
                continue  # Unique combo unavailable

            ret.append((mode_id, unique_combo_data.action_id))

        if not ret:
            ret.append(default_variant_by_weapon)

        if self.has_unique_dragon:
            dragon_data = self.get_dragon_data(asset_manager.asset_dragon_data)

            # Constant -1 for unique dragon
            ret.append((-1, dragon_data.normal_attack_action_id))

        return ret

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
            element=Element(data["_ElementalType"]),
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
            mode_change_type=ModeChangeType(data["_ModeChangeType"]),
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
            is_dragon_drive=bool(data["_WinFaceMouthMotion"]),  # ?????
            is_playable=bool(data["_IsPlayable"]),
            max_friendship_point=data["_MaxFriendshipPoint"],
            grow_material_start=cls.parse_datetime(data["_GrowMaterialOnlyStartDate"]),
            grow_material_end=cls.parse_datetime(data["_GrowMaterialOnlyEndDate"]),
            grow_material_id=data["_GrowMaterialId"],
            cv_en_label=data["_CvInfoEn"],
            cv_jp_label=data["_CvInfo"],
            release_date=cls.parse_datetime(data["_ReleaseStartDate"])
        )


class CharaDataAsset(UnitAsset[CharaDataEntry], MasterAssetBase[CharaDataEntry]):
    """Character data asset class."""

    asset_file_name = "CharaData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(CharaDataParser, file_location, asset_dir=asset_dir, file_like=file_like)


class CharaDataParser(MasterParserBase[CharaDataEntry]):
    """Class to parse the character data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, CharaDataEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: CharaDataEntry.parse_raw(value) for key, value in entries.items()}
