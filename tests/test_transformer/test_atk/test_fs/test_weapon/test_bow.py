from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Bow Lv. 1 (600005)
    data = transformer_atk.transform_normal_attack_or_fs(600005).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.28] * 8
    assert combo_1.sp_gain == 460
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [3.0] * 8


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Bow Lv. 2 (600005)
    data = transformer_atk.transform_normal_attack_or_fs(600005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.31] * 8
    assert combo_1.sp_gain == 460
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [3.0] * 8
