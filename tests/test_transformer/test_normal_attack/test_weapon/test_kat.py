from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Blade Lv. 1 (200000)
    normal_attack_data = transformer_atk.transform_normal_attack(200000)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [1.16]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [1.164]
    assert combo_2.sp_gain == 130
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [0.76] * 2
    assert combo_3.sp_gain == 220
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [1.55]
    assert combo_4.sp_gain == 360
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [1.72] * 2
    assert combo_5.sp_gain == 900
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 2


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Blade Lv. 2 (200000)
    normal_attack_data = transformer_atk.transform_normal_attack(200000, 2)

    combo_1 = normal_attack_data.combos[0]
    assert combo_1.mods == [1.28]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data.combos[1]
    assert combo_2.mods == [1.28]
    assert combo_2.sp_gain == 130
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = normal_attack_data.combos[2]
    assert combo_3.mods == [0.84] * 2
    assert combo_3.sp_gain == 220
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2

    combo_4 = normal_attack_data.combos[3]
    assert combo_4.mods == [1.71]
    assert combo_4.sp_gain == 360
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data.combos[4]
    assert combo_5.mods == [1.89] * 2
    assert combo_5.sp_gain == 900
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 2
