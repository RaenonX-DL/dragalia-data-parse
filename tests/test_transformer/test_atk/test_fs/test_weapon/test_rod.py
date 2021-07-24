from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Wand Lv. 1 (700005)
    data = transformer_atk.transform_normal_attack_or_fs(700005).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.81] * 2
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [4.0] * 2


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Wand Lv. 2 (700005)
    data = transformer_atk.transform_normal_attack_or_fs(700005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.9] * 2
    assert combo_1.sp_gain == 400
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [4.0] * 2
