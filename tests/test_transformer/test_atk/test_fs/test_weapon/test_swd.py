from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Sword Lv. 1 (100005)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(100005).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [1.04]
    assert combo_1.sp_gain == 345
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [8.0]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Sword Lv. 2 (100005)
    data = transformer_atk.transform_normal_attack_or_fs(100005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.15]
    assert combo_1.sp_gain == 345
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [8.0]
