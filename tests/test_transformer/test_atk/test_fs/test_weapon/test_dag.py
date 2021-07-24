from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Dagger Lv. 1 (300005)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(300005).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [0.423] * 3
    assert combo_1.sp_gain == 288
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [8.4, 8.4, 4.2]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Dagger Lv. 2 (300005)
    data = transformer_atk.transform_normal_attack_or_fs(300005, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.47] * 3
    assert combo_1.sp_gain == 288
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [8.4, 8.4, 4.2]
