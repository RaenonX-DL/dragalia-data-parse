from dlparse.transformer import AttackingActionTransformer


def test_default_fs_lv1(transformer_atk: AttackingActionTransformer):
    # Zhu Bajie FS (400205)
    # https://dragalialost.wiki/w/Zhu_Bajie
    data = transformer_atk.transform_normal_attack_or_fs(400205).with_condition()

    charge_1 = data[0]
    assert charge_1.mods == [1.86]
    assert charge_1.sp_gain == 600
    assert charge_1.utp_gain == 0
    assert charge_1.od_rate == [2.15]

    charge_2 = data[1]
    assert charge_2.mods == [2.67]
    assert charge_2.sp_gain == 960
    assert charge_2.utp_gain == 0
    assert charge_2.od_rate == [1.95]

    charge_3 = data[2]
    assert charge_3.mods == [3.45]
    assert charge_3.sp_gain == 1400
    assert charge_3.utp_gain == 0
    assert charge_3.od_rate == [1.75]


def test_default_fs_lv2(transformer_atk: AttackingActionTransformer):
    # Zhu Bajie FS (400205)
    # https://dragalialost.wiki/w/Zhu_Bajie
    data = transformer_atk.transform_normal_attack_or_fs(400205, 2).with_condition()

    charge_1 = data[0]
    assert charge_1.mods == [2.07]
    assert charge_1.sp_gain == 600
    assert charge_1.utp_gain == 0
    assert charge_1.od_rate == [2.15]

    charge_2 = data[1]
    assert charge_2.mods == [2.97]
    assert charge_2.sp_gain == 960
    assert charge_2.utp_gain == 0
    assert charge_2.od_rate == [1.95]

    combo_3 = data[2]
    assert combo_3.mods == [3.84]
    assert combo_3.sp_gain == 1400
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.75]
