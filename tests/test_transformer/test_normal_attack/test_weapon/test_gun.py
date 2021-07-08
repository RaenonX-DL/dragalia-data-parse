from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack_long(transformer_atk: AttackingActionTransformer):
    # Manacaster (900000 - Long)
    normal_attack_data = transformer_atk.transform_normal_attack(900000)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [0.67] * 5
    assert combo_1.sp_gain == 545
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 5

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [0.67] * 5
    assert combo_2.sp_gain == 545
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 5


def test_default_normal_attack_close(transformer_atk: AttackingActionTransformer):
    # Manacaster (900100 - Close)
    normal_attack_data = transformer_atk.transform_normal_attack(900100)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [0.48] * 8
    assert combo_1.sp_gain == 340
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 8

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [0.48] * 8
    assert combo_2.sp_gain == 340
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 8


def test_default_normal_attack_rapid(transformer_atk: AttackingActionTransformer):
    # Manacaster (900200 - Rapid)
    normal_attack_data = transformer_atk.transform_normal_attack(900200)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [0.45] * 3
    assert combo_1.sp_gain == 200
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 3

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [0.60] * 3
    assert combo_2.sp_gain == 200
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 3

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [0.60] * 5
    assert combo_3.sp_gain == 200
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 5
