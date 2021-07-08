from dlparse.transformer import AttackingActionTransformer


def test_enhanced_normal_attack(transformer_atk: AttackingActionTransformer):
    # Nino (10150305)
    # - Mode 95: Unique Transform
    # - Unique Combo 67
    # - Action ID 101100
    normal_attack_data = transformer_atk.transform_normal_attack(101100)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [0.15, 0.9]
    assert combo_1.sp_gain == 150
    assert combo_1.utp_gain == 45
    assert combo_1.od_rate == [1.0, 1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [0.15, 0.96]
    assert combo_2.sp_gain == 150
    assert combo_2.utp_gain == 45
    assert combo_2.od_rate == [1.0, 1.0]

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [0.15, 1.14]
    assert combo_3.sp_gain == 196
    assert combo_3.utp_gain == 85
    assert combo_3.od_rate == [1.0, 1.0]

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [0.15, 0.15, 1.2]
    assert combo_4.sp_gain == 265
    assert combo_4.utp_gain == 180
    assert combo_4.od_rate == [1.0, 1.0, 1.0]

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [0.15, 0.15, 0.15, 1.8]
    assert combo_5.sp_gain == 391
    assert combo_5.utp_gain == 250
    assert combo_5.od_rate == [1.0, 1.0, 1.0, 1.0]
