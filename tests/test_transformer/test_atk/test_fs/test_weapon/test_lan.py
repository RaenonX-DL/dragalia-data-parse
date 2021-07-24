from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Lance Lv. 1 (500005)
    data = transformer_atk.transform_normal_attack_or_fs(500005).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.27] * 5
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [5.2] * 4 + [6.2]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Lance Lv. 2 (500005)
    data = transformer_atk.transform_normal_attack_or_fs(500005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.3] * 5
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [5.2] * 4 + [6.2]
