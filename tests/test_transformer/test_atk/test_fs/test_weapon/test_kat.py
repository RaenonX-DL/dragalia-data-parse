from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Blade Lv. 1 (200005)
    data = transformer_atk.transform_normal_attack_or_fs(200005).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.83]
    assert combo_1.sp_gain == 200
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [6.0]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Blade Lv. 2 (200005)
    data = transformer_atk.transform_normal_attack_or_fs(200005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.92]
    assert combo_1.sp_gain == 200
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [6.0]
