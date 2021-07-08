from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Axe Lv. 1 (400000)
    normal_attack_data = transformer_atk.transform_normal_attack(400000)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [1.37]
    assert combo_1.sp_gain == 200
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [1.46]
    assert combo_2.sp_gain == 240
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [2.45]
    assert combo_3.sp_gain == 360
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0]

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [2.59]
    assert combo_4.sp_gain == 380
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [2.74]
    assert combo_5.sp_gain == 420
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Axe Lv. 2 (400000)
    normal_attack_data = transformer_atk.transform_normal_attack(400000, 2)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [1.51]
    assert combo_1.sp_gain == 200
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [1.61]
    assert combo_2.sp_gain == 240
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [2.70]
    assert combo_3.sp_gain == 360
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0]

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [2.85]
    assert combo_4.sp_gain == 380
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [3.01]
    assert combo_5.sp_gain == 420
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]