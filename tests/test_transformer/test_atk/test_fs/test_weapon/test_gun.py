from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack_long(transformer_atk: AttackingActionTransformer):
    # Manacaster (900005 - Long)
    data = transformer_atk.transform_normal_attack_or_fs(900005).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.62]
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [4.0]


def test_default_normal_attack_long_lv_2(transformer_atk: AttackingActionTransformer):
    # Manacaster (900005 - Long)
    data = transformer_atk.transform_normal_attack_or_fs(900005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.8]
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [4.0]


def test_default_normal_attack_close(transformer_atk: AttackingActionTransformer):
    # Manacaster (900105 - Close)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(900105).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [0.35] * 10
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [2.0] * 10


def test_default_normal_attack_close_lv_2(transformer_atk: AttackingActionTransformer):
    # Manacaster (900105 - Close)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(900105, 2).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [0.4] * 10
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [2.0] * 10


def test_default_normal_attack_rapid(transformer_atk: AttackingActionTransformer):
    # Manacaster (900205 - Rapid)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(900205).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [0.41] * 10
    assert combo_1.sp_gain == 90
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [0.3] * 10


def test_default_normal_attack_rapid_lv_2(transformer_atk: AttackingActionTransformer):
    # Manacaster (900205 - Rapid)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(900205, 2).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [0.5] * 10
    assert combo_1.sp_gain == 90
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [0.3] * 10
