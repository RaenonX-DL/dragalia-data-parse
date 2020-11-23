from dlparse.mono.asset import CharaDataEntry, CharaModeAsset, TextAsset


def create_dummy(**kwargs) -> CharaDataEntry:
    params = {
        "id": -1,
        "name_label": "Dummy",
        "second_name_label": "Dummy",
        "emblem_id": -1,
        "weapon_type_id": -1,
        "rarity": -1,
        "max_limit_break_count": -1,
        "element_id": -1,
        "chara_type_id": -1,
        "chara_base_id": -1,
        "chara_variation_id": -1,
        "max_hp": -1,
        "max_hp_1": -1,
        "plus_hp_0": -1,
        "plus_hp_1": -1,
        "plus_hp_2": -1,
        "plus_hp_3": -1,
        "plus_hp_4": -1,
        "plus_hp_5": -1,
        "mc_full_bonus_hp": -1,
        "max_atk": -1,
        "max_atk_1": -1,
        "plus_atk_0": -1,
        "plus_atk_1": -1,
        "plus_atk_2": -1,
        "plus_atk_3": -1,
        "plus_atk_4": -1,
        "plus_atk_5": -1,
        "mc_full_bonus_atk": -1,
        "def_coef": -1,
        "mode_change_id": -1,
        "mode_1_id": 0,
        "mode_2_id": 0,
        "mode_3_id": 0,
        "mode_4_id": 0,
        "keep_mode_on_revive": False,
        "combo_original_id": -1,
        "combo_mode_1_id": -1,
        "combo_mode_2_id": -1,
        "skill_1_id": -1,
        "skill_2_id": -1,
        "passive_1_lv_1_id": -1,
        "passive_1_lv_2_id": -1,
        "passive_1_lv_3_id": -1,
        "passive_1_lv_4_id": -1,
        "passive_2_lv_1_id": -1,
        "passive_2_lv_2_id": -1,
        "passive_2_lv_3_id": -1,
        "passive_2_lv_4_id": -1,
        "passive_3_lv_1_id": -1,
        "passive_3_lv_2_id": -1,
        "passive_3_lv_3_id": -1,
        "passive_3_lv_4_id": -1,
        "ex_1_id": -1,
        "ex_2_id": -1,
        "ex_3_id": -1,
        "ex_4_id": -1,
        "ex_5_id": -1,
        "cex_1_id": -1,
        "cex_2_id": -1,
        "cex_3_id": -1,
        "cex_4_id": -1,
        "cex_5_id": -1,
        "fs_type_id": -1,
        "fs_count_max": -1,
        "ss_cost_max_self": -1,
        "ss_skill_id": -1,
        "ss_skill_level": -1,
        "ss_skill_cost": -1,
        "ss_skill_relation_id": -1,
        "ss_release_item_id": -1,
        "ss_release_item_quantity": -1,
        "unique_dragon_id": -1,
        "is_dragon_drive": False,
        "is_playable": False,
        "max_friendship_point": -1,
        "grow_material_start": None,
        "grow_material_end": None,
        "grow_material_id": -1,
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


def test_get_chara_name_use_main(text_asset: TextAsset):
    entry = create_dummy(name_label="CHARA_NAME_10840301", second_name_label="CHARA_NAME_COMMENT_10840301")
    assert entry.get_chara_name(text_asset) == "ルーエン"


def test_get_chara_name_use_second(text_asset: TextAsset):
    entry = create_dummy(name_label="CHARA_NAME_10150302", second_name_label="CHARA_NAME_COMMENT_10150302")
    assert entry.get_chara_name(text_asset) == "エルフィリス（ウエディングVer.）"


def test_get_skill_id_names(chara_mode_asset: CharaModeAsset, text_asset: TextAsset):
    entry = create_dummy(skill_1_id=1, skill_2_id=2)
    assert entry.get_skill_identifiers(chara_mode_asset, text_asset=text_asset) == [(1, "S1"), (2, "S2")]


def test_get_skill_id_names_with_mode(chara_mode_asset: CharaModeAsset, text_asset: TextAsset):
    entry = create_dummy(skill_1_id=1, skill_2_id=2, mode_2_id=12)
    assert entry.get_skill_identifiers(chara_mode_asset, text_asset=text_asset) == [
        (1, "S1"), (2, "S2"),
        (103505033, "S1 (服わざる伴侶)"), (103505034, "S2 (服わざる伴侶)")
    ]
