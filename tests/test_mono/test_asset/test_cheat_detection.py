import os

from dlparse.mono.asset import CheatDetectionAsset, CheatDetectionEntry
from tests.static import PATH_LOCAL_DIR_MASTER_ASSET


def test_parse_cheat_detection_explicit_path():
    cheat_detection = CheatDetectionAsset(os.path.join(PATH_LOCAL_DIR_MASTER_ASSET, "CheatDetectionParam.json"))

    entry = CheatDetectionEntry(
        id=1,
        max_enemy_damage=100000000,
        max_enemy_break_damage=100000000,
        max_enemy_player_distance=35,
        max_player_heal=25000,
        max_player_move_speed=10
    )

    assert len(cheat_detection) == 1
    assert cheat_detection.get_data_by_id(1) == entry
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 100000000) == [entry]
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 87) == []


def test_parse_cheat_detection_implicit_path():
    cheat_detection = CheatDetectionAsset(asset_dir=PATH_LOCAL_DIR_MASTER_ASSET)

    entry = CheatDetectionEntry(
        id=1,
        max_enemy_damage=100000000,
        max_enemy_break_damage=100000000,
        max_enemy_player_distance=35,
        max_player_heal=25000,
        max_player_move_speed=10
    )

    assert len(cheat_detection) == 1
    assert cheat_detection.get_data_by_id(1) == entry
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 100000000) == [entry]
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 87) == []
