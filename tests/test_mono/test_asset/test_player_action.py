from dlparse.mono.asset import PlayerActionPrefab


def test_label_omission():
    assert not PlayerActionPrefab.is_effective_label("CMN_AVOID")
    assert not PlayerActionPrefab.is_effective_label("CMN_AVOID_LV01")
    assert not PlayerActionPrefab.is_effective_label("CMN_AVOID_LV04")
    assert PlayerActionPrefab.is_effective_label("DAG_130_04_H01_LV01")
