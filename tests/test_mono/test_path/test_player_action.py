from dlparse.mono.loader import PlayerActionFileLoader


def test_file_action_id_extraction():
    assert PlayerActionFileLoader.extract_action_id("PlayerAction_00400707.prefab.json") == 400707
    assert PlayerActionFileLoader.extract_action_id("PlayerAction_20400707.prefab.json") == 20400707
    assert PlayerActionFileLoader.extract_action_id("PlayerAction_99400707.prefab.json") == 99400707
