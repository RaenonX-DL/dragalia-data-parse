from dlparse.mono.asset import CharaDataEntry
from dlparse.mono.manager import AssetManager


def create_dummy(**kwargs) -> CharaDataEntry:
    params = {
        "id": 0,
        "name_label": "Dummy",
        "name_label_2": "Dummy",
        "emblem_id": 0,
        "weapon_type_id": 0,
        "rarity": 0,
        "max_limit_break_count": 0,
        "element_id": 0,
        "chara_type_id": 0,
        "chara_base_id": 0,
        "chara_variation_id": 0,
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
        "mode_change_type": 0,
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
        "win_face_mouth_id": 0
    }

    params.update(kwargs)

    return CharaDataEntry(**params)


def test_is_70_mc():
    entry = create_dummy(max_limit_break_count=4)
    assert not entry.is_70_mc

    entry = create_dummy(max_limit_break_count=5)
    assert entry.is_70_mc


def test_max_hp_50():
    entry = create_dummy(
        max_limit_break_count=4,
        max_hp=1, max_hp_1=256,
        plus_hp_0=2, plus_hp_1=4, plus_hp_2=8, plus_hp_3=16, plus_hp_4=32, plus_hp_5=64,
        mc_full_bonus_hp=128
    )

    assert not entry.is_70_mc
    assert entry.max_hp_at_50 == 191
    assert entry.max_hp_at_70 == 510
    assert entry.max_hp_current == 191


def test_max_hp_70():
    entry = create_dummy(
        max_limit_break_count=5,
        max_hp=1, max_hp_1=256,
        plus_hp_0=2, plus_hp_1=4, plus_hp_2=8, plus_hp_3=16, plus_hp_4=32, plus_hp_5=64,
        mc_full_bonus_hp=128
    )

    assert entry.is_70_mc
    assert entry.max_hp_at_50 == 191
    assert entry.max_hp_at_70 == 510
    assert entry.max_hp_current == 510


def test_max_atk_50():
    entry = create_dummy(
        max_limit_break_count=4,
        max_atk=1, max_atk_1=256,
        plus_atk_0=2, plus_atk_1=4, plus_atk_2=8, plus_atk_3=16, plus_atk_4=32, plus_atk_5=64,
        mc_full_bonus_atk=128
    )

    assert not entry.is_70_mc
    assert entry.max_atk_at_50 == 191
    assert entry.max_atk_at_70 == 510
    assert entry.max_atk_current == 191


def test_max_atk_70():
    entry = create_dummy(
        max_limit_break_count=5,
        max_atk=1, max_atk_1=256,
        plus_atk_0=2, plus_atk_1=4, plus_atk_2=8, plus_atk_3=16, plus_atk_4=32, plus_atk_5=64,
        mc_full_bonus_atk=128
    )

    assert entry.is_70_mc
    assert entry.max_atk_at_50 == 191
    assert entry.max_atk_at_70 == 510
    assert entry.max_atk_current == 510


def test_mode_ids():
    entry = create_dummy(mode_1_id=1, mode_2_id=2, mode_3_id=3, mode_4_id=4)
    assert entry.mode_ids == [1, 2, 3, 4]

    entry = create_dummy(mode_1_id=0, mode_2_id=2, mode_3_id=0, mode_4_id=0)
    assert entry.mode_ids == [2]

    entry = create_dummy(mode_1_id=0, mode_2_id=0, mode_3_id=0, mode_4_id=0)
    assert entry.mode_ids == []


def test_custom_id():
    entry = create_dummy(chara_base_id=100002, chara_variation_id=6)
    assert entry.custom_id == "100002/6"

    entry = create_dummy(chara_base_id=100007, chara_variation_id=1)
    assert entry.custom_id == "100007/1"

    entry = create_dummy(chara_base_id=100011, chara_variation_id=11)
    assert entry.custom_id == "100011/11"


def test_get_chara_name_use_main(asset_manager: AssetManager):
    entry = create_dummy(name_label="CHARA_NAME_10840301", name_label_2="CHARA_NAME_COMMENT_10840301")
    assert entry.get_chara_name(asset_manager.asset_text) == "ルーエン"


def test_get_chara_name_use_second(asset_manager: AssetManager):
    entry = create_dummy(name_label="CHARA_NAME_10150302", name_label_2="CHARA_NAME_COMMENT_10150302")
    assert entry.get_chara_name(asset_manager.asset_text) == "エルフィリス（ウエディングVer.）"
