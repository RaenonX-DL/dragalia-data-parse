from dlparse.mono.manager import AssetManager

from .utils import create_dummy


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


def test_get_chara_name_use_main(asset_manager: AssetManager):
    entry = create_dummy(name_label="CHARA_NAME_10840301", name_label_2="CHARA_NAME_COMMENT_10840301")
    assert entry.get_name(asset_manager.asset_text_multi) == "ルーエン"


def test_get_chara_name_use_second(asset_manager: AssetManager):
    entry = create_dummy(name_label="CHARA_NAME_10150302", name_label_2="CHARA_NAME_COMMENT_10150302")
    assert entry.get_name(asset_manager.asset_text_multi) == "エルフィリス（ウエディングVer.）"
