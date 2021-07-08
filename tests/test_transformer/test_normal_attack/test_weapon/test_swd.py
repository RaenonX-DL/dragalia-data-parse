from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Sword Lv. 1 (100000)
    normal_attack_data = transformer_atk.transform_normal_attack(100000)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [0.90]
    assert combo_1.sp_gain == 150
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [0.96]
    assert combo_2.sp_gain == 150
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [1.14]
    assert combo_3.sp_gain == 196
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0]

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [1.20]
    assert combo_4.sp_gain == 265
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [1.8]
    assert combo_5.sp_gain == 391
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Sword Lv. 2 (100000)
    normal_attack_data = transformer_atk.transform_normal_attack(100000, 2)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [1.08]
    assert combo_1.sp_gain == 150
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [1.15]
    assert combo_2.sp_gain == 150
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [1.37]
    assert combo_3.sp_gain == 196
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0]

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [1.44]
    assert combo_4.sp_gain == 265
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [2.16]
    assert combo_5.sp_gain == 391
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]
