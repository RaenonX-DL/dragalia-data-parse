from dlparse.enums import Element, ModeChangeType, Weapon
from dlparse.mono.asset import CharaDataEntry


def create_dummy(**kwargs) -> CharaDataEntry:
    params = {
        "id": 0,
        "name_label": "Dummy",
        "name_label_2": "Dummy",
        "emblem_id": 0,
        "weapon": Weapon.SWD,
        "rarity": 0,
        "max_limit_break_count": 0,
        "element": Element.UNKNOWN,
        "chara_type_id": 0,
        "base_id": 0,
        "variation_id": 0,
        "max_hp": 0,
        "max_hp_1": 0,
        "plus_hp_0": 0,
        "plus_hp_1": 0,
        "plus_hp_2": 0,
        "plus_hp_3": 0,
        "plus_hp_4": 0,
        "plus_hp_5": 0,
        "mc_full_bonus_hp": 0,
        "max_atk": 0,
        "max_atk_1": 0,
        "plus_atk_0": 0,
        "plus_atk_1": 0,
        "plus_atk_2": 0,
        "plus_atk_3": 0,
        "plus_atk_4": 0,
        "plus_atk_5": 0,
        "mc_full_bonus_atk": 0,
        "def_coef": 0,
        "mode_change_type": ModeChangeType.NONE,
        "mode_1_id": 0,
        "mode_2_id": 0,
        "mode_3_id": 0,
        "mode_4_id": 0,
        "keep_mode_on_revive": False,
        "combo_original_id": 0,
        "combo_mode_1_id": 0,
        "combo_mode_2_id": 0,
        "skill_1_id": 0,
        "skill_2_id": 0,
        "ability_1_lv_1_id": 0,
        "ability_1_lv_2_id": 0,
        "ability_1_lv_3_id": 0,
        "ability_1_lv_4_id": 0,
        "ability_2_lv_1_id": 0,
        "ability_2_lv_2_id": 0,
        "ability_2_lv_3_id": 0,
        "ability_2_lv_4_id": 0,
        "ability_3_lv_1_id": 0,
        "ability_3_lv_2_id": 0,
        "ability_3_lv_3_id": 0,
        "ability_3_lv_4_id": 0,
        "ex_1_id": 0,
        "ex_2_id": 0,
        "ex_3_id": 0,
        "ex_4_id": 0,
        "ex_5_id": 0,
        "cex_1_id": 0,
        "cex_2_id": 0,
        "cex_3_id": 0,
        "cex_4_id": 0,
        "cex_5_id": 0,
        "fs_type_id": 0,
        "fs_count_max": 0,
        "ss_cost_max_self": 0,
        "ss_skill_id": 0,
        "ss_skill_num": 1,
        "ss_skill_cost": 0,
        "ss_skill_relation_id": 0,
        "ss_release_item_id": 0,
        "ss_release_item_quantity": 0,
        "unique_dragon_id": 0,
        "is_dragon_drive": False,
        "is_playable": False,
        "max_friendship_point": 0,
        "grow_material_start": None,
        "grow_material_end": None,
        "grow_material_id": 0,
        "unique_dragon_inherit_skill_lv": 0,
        "unique_weapon_id": 0,
        "win_face_eye_id": 0,
        "win_face_mouth_id": 0,
        "cv_en_label": "DummyCvEn",
        "cv_jp_label": "DummyCvJp",
        "release_date": "2021/01/01 00:00:00"
    }

    params.update(kwargs)

    return CharaDataEntry(**params)
