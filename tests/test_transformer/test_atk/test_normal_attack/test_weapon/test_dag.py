from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Dagger Lv. 1 (300000)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(300000).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [0.90]
    assert combo_1.sp_gain == 144
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data[1]
    assert combo_2.mods == [0.46, 0.46]
    assert combo_2.sp_gain == 144
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0, 1.0]

    combo_3 = normal_attack_data[2]
    assert combo_3.mods == [0.65, 0.65]
    assert combo_3.sp_gain == 264
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0, 1.0]

    combo_4 = normal_attack_data[3]
    assert combo_4.mods == [1.43]
    assert combo_4.sp_gain == 288
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data[4]
    assert combo_5.mods == [1.8]
    assert combo_5.sp_gain == 480
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Dagger Lv. 2 (300000)
    data = transformer_atk.transform_normal_attack_or_fs(300000, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.08]
    assert combo_1.sp_gain == 144
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == [0.55, 0.55]
    assert combo_2.sp_gain == 144
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0, 1.0]

    combo_3 = data[2]
    assert combo_3.mods == [0.78, 0.78]
    assert combo_3.sp_gain == 264
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0, 1.0]

    combo_4 = data[3]
    assert combo_4.mods == [1.71]
    assert combo_4.sp_gain == 288
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = data[4]
    assert combo_5.mods == [2.16]
    assert combo_5.sp_gain == 480
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]
