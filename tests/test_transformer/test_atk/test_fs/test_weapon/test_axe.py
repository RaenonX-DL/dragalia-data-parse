from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Axe Lv. 1 (400005)
    data = transformer_atk.transform_normal_attack_or_fs(400005).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.73]
    assert combo_1.sp_gain == 300
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [3.08]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Axe Lv. 2 (400005)
    data = transformer_atk.transform_normal_attack_or_fs(400005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.92]
    assert combo_1.sp_gain == 300
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [3.08]
