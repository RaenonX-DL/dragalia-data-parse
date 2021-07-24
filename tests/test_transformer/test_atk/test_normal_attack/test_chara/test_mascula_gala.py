import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_normal_attack(transformer_atk: AttackingActionTransformer):
    # Gala Mascula (10250203)
    # - Mode 93: Normal
    # - Unique Combo 65
    # - Action ID 202700
    conditions = ConditionComposite()
    data = transformer_atk.transform_normal_attack_or_fs(202700).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [0.13] * 2 + [0.38]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 3
    assert combo_1.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_2 = data[1]
    assert combo_2.mods == [0.19, 0.56]
    assert combo_2.sp_gain == 220
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 2
    assert combo_2.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_3 = data[2]
    assert combo_3.mods == [0.13] * 3 + [0.37]
    assert combo_3.sp_gain == 360
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 4
    assert combo_3.cancel_to_next_action_sec == pytest.approx(0.90, rel=1E-2)

    combo_4 = data[3]
    assert combo_4.mods == [0.57, 1.72]
    assert combo_4.sp_gain == 660
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 2
    assert combo_4.cancel_to_next_action_sec == pytest.approx(1.17, rel=1E-2)


def test_s1_normal_attack(transformer_atk: AttackingActionTransformer):
    # Gala Mascula (10250203)
    # - Mode 93: Normal
    # - Unique Combo 65
    # - Action ID 202700
    conditions = ConditionComposite(Condition.SELF_GMASCULA_S1_LV3)
    data = transformer_atk.transform_normal_attack_or_fs(202700).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [0.13] * 4 + [0.38]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 5
    assert combo_1.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_2 = data[1]
    assert combo_2.mods == [0.19] * 3 + [0.56]
    assert combo_2.sp_gain == 220
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 4
    assert combo_2.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_3 = data[2]
    assert combo_3.mods == [0.13] * 7 + [0.37]
    assert combo_3.sp_gain == 360
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 8
    assert combo_3.cancel_to_next_action_sec == pytest.approx(0.90, rel=1E-2)

    combo_4 = data[3]
    assert combo_4.mods == [0.57] * 3 + [1.72]
    assert combo_4.sp_gain == 660
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 4
    assert combo_4.cancel_to_next_action_sec == pytest.approx(1.17, rel=1E-2)


def test_s2_enhanced_attack(transformer_atk: AttackingActionTransformer):
    # Gala Mascula (10250203)
    # - Mode 94: S2 Effective
    # - Unique Combo 66
    # - Action ID 202800
    conditions = ConditionComposite()
    data = transformer_atk.transform_normal_attack_or_fs(202800).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [0.16] + [0.19] * 3 + [0.16] + [0.45]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 6
    assert combo_1.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_2 = data[1]
    assert combo_2.mods == [0.23] + [0.19] * 3 + [0.67]
    assert combo_2.sp_gain == 220
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 5
    assert combo_2.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_3 = data[2]
    assert combo_3.mods == [0.16] + [0.19] * 3 + [0.16] * 4 + [0.44]
    assert combo_3.sp_gain == 360
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 9
    assert combo_3.cancel_to_next_action_sec == pytest.approx(0.90, rel=1E-2)

    combo_4 = data[3]
    assert combo_4.mods == [0.68] + [0.19] * 3 + [0.68] * 1 + [2.03]
    assert combo_4.sp_gain == 660
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 6
    assert combo_4.cancel_to_next_action_sec == pytest.approx(1.17, rel=1E-2)


def test_s2_enhanced_attack_with_s1(transformer_atk: AttackingActionTransformer):
    # Gala Mascula (10250203)
    # - Mode 94: S2 Effective
    # - Unique Combo 66
    # - Action ID 202800
    conditions = ConditionComposite(Condition.SELF_GMASCULA_S1_LV3)
    data = transformer_atk.transform_normal_attack_or_fs(202800).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [0.16] + [0.19] * 6 + [0.16] * 3 + [0.45]
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 11
    assert combo_1.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_2 = data[1]
    assert combo_2.mods == [0.23] + [0.19] * 6 + [0.23] * 2 + [0.67]
    assert combo_2.sp_gain == 220
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 10
    assert combo_2.cancel_to_next_action_sec == pytest.approx(0.63, rel=1E-2)

    combo_3 = data[2]
    assert combo_3.mods == ([0.16] + [0.19] * 3) * 2 + [0.16] * 7 + [0.44]
    assert combo_3.sp_gain == 360
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 16
    assert combo_3.cancel_to_next_action_sec == pytest.approx(0.90, rel=1E-2)

    combo_4 = data[3]
    assert combo_4.mods == [0.68] + ([0.68] + [0.19] * 3) * 2 + [0.68] + [2.03]
    assert combo_4.sp_gain == 660
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 11
    assert combo_4.cancel_to_next_action_sec == pytest.approx(1.17, rel=1E-2)
