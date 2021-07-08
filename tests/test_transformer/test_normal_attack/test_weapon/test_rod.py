from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Wand Lv. 1 (700000)
    normal_attack_data = transformer_atk.transform_normal_attack(700000)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [1.18]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [0.64] * 2
    assert combo_2.sp_gain == 200
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 2

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [0.43] * 3
    assert combo_3.sp_gain == 240
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 3

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [0.94] * 2
    assert combo_4.sp_gain == 430
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 2

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [0.74] + [0.43] * 4
    assert combo_5.sp_gain == 600
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 5


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Wand Lv. 2 (700000)
    normal_attack_data = transformer_atk.transform_normal_attack(700000, 2)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [1.36]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [0.74] * 2
    assert combo_2.sp_gain == 200
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 2

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [0.49] * 3
    assert combo_3.sp_gain == 240
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 3

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [1.08] * 2
    assert combo_4.sp_gain == 430
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 2

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [0.85] + [0.49] * 4
    assert combo_5.sp_gain == 600
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 5
