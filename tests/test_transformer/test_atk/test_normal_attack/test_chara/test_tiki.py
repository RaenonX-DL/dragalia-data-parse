from dlparse.transformer import AttackingActionTransformer


def test_human_form(transformer_atk: AttackingActionTransformer):
    # Tiki (10350203)
    # - Mode 19: Divine Dragon
    # - Unique Combo 15
    # - Action ID 300400
    data = transformer_atk.transform_normal_attack(300400).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.08]
    assert combo_1.sp_gain == 88
    assert combo_1.utp_gain == 2
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == [0.18]
    assert combo_2.sp_gain == 141
    assert combo_2.utp_gain == 3
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == [0.13]
    assert combo_3.sp_gain == 178
    assert combo_3.utp_gain == 4
    assert combo_3.od_rate == [1.0]

    combo_4 = data[3]
    assert combo_4.mods == [0.37]
    assert combo_4.sp_gain == 350
    assert combo_4.utp_gain == 5
    assert combo_4.od_rate == [1.0]

    combo_5 = data[4]
    assert combo_5.mods == [0.40]
    assert combo_5.sp_gain == 367
    assert combo_5.utp_gain == 6
    assert combo_5.od_rate == [1.0]
