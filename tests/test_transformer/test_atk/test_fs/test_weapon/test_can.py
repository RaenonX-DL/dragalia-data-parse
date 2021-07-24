from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Staff Lv. 1 (800005)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(800005).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [0.55] * 4
    assert combo_1.sp_gain == 580
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [4.2] * 4


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Staff Lv. 2 (800005)
    data = transformer_atk.transform_normal_attack_or_fs(800005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.61] * 4
    assert combo_1.sp_gain == 580
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [4.2] * 4
