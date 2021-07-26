from dlparse.transformer import AttackingActionTransformer


def test_default_fs_lv1(transformer_atk: AttackingActionTransformer):
    # MH Sarisse FS (698005)
    # https://dragalialost.wiki/w/Hunter_Sarisse
    data = transformer_atk.transform_normal_attack_or_fs(698005).with_condition()

    charge_1 = data[0]
    assert charge_1.mods == [1.452 * 0.3 ** hit_count for hit_count in range(5) for _ in range(3)]
    assert charge_1.sp_gain == 500
    assert charge_1.utp_gain == 0
    assert charge_1.od_rate == [1.25]

    charge_2 = data[1]
    assert charge_2.mods == [1.65 * 0.3 ** hit_count for hit_count in range(5) for _ in range(3)]
    assert charge_2.sp_gain == 710
    assert charge_2.utp_gain == 0
    assert charge_2.od_rate == [1.25]

    charge_3 = data[2]
    assert charge_3.mods == [1.848 * 0.3 ** hit_count for hit_count in range(5) for _ in range(4)]
    assert charge_3.sp_gain == 920
    assert charge_3.utp_gain == 0
    assert charge_3.od_rate == [1.25]

    charge_4 = data[2]
    assert charge_4.mods == [2.552 * 0.3 ** hit_count for hit_count in range(5) for _ in range(4)]
    assert charge_4.sp_gain == 1140
    assert charge_4.utp_gain == 0
    assert charge_4.od_rate == [1.25]


def test_default_fs_lv2(transformer_atk: AttackingActionTransformer):
    # MH Sarisse FS (698005)
    # https://dragalialost.wiki/w/Hunter_Sarisse
    data = transformer_atk.transform_normal_attack_or_fs(698005, 2).with_condition()

    charge_1 = data[0]
    assert charge_1.mods == [1.628 * 0.3 ** hit_count for hit_count in range(5) for _ in range(3)]
    assert charge_1.sp_gain == 500
    assert charge_1.utp_gain == 0
    assert charge_1.od_rate == [1.25]

    charge_2 = data[1]
    assert charge_2.mods == [1.848 * 0.3 ** hit_count for hit_count in range(5) for _ in range(3)]
    assert charge_2.sp_gain == 710
    assert charge_2.utp_gain == 0
    assert charge_2.od_rate == [1.25]

    charge_3 = data[2]
    assert charge_3.mods == [2.068 * 0.3 ** hit_count for hit_count in range(5) for _ in range(4)]
    assert charge_3.sp_gain == 920
    assert charge_3.utp_gain == 0
    assert charge_3.od_rate == [1.25]

    charge_4 = data[2]
    assert charge_4.mods == [2.838 * 0.3 ** hit_count for hit_count in range(5) for _ in range(4)]
    assert charge_4.sp_gain == 1140
    assert charge_4.utp_gain == 0
    assert charge_4.od_rate == [1.25]
