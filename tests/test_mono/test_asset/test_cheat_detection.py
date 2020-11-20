import os

from dlparse.mono.asset import CheatDetectionAsset, CheatDetectionEntry


def test_parse_cheat_detection_explicit_path(asset_master_dir):
    cheat_detection = CheatDetectionAsset(os.path.join(asset_master_dir, "CheatDetectionParam.json"))

    entry = CheatDetectionEntry(
        id=1,
        max_enemy_damage=50000000,
        max_enemy_break_damage=60000000,
        max_enemy_player_distance=35,
        max_player_heal=25000,
        max_player_move_speed=10
    )

    assert len(cheat_detection) == 1
    assert cheat_detection.get_data_by_id(1) == entry
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 50000000) == [entry]
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 87) == []


def test_parse_cheat_detection_implicit_path(asset_master_dir):
    cheat_detection = CheatDetectionAsset(asset_dir=asset_master_dir)

    entry = CheatDetectionEntry(
        id=1,
        max_enemy_damage=50000000,
        max_enemy_break_damage=60000000,
        max_enemy_player_distance=35,
        max_player_heal=25000,
        max_player_move_speed=10
    )

    assert len(cheat_detection) == 1
    assert cheat_detection.get_data_by_id(1) == entry
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 50000000) == [entry]
    assert cheat_detection.filter(lambda data: data.max_enemy_damage == 87) == []
