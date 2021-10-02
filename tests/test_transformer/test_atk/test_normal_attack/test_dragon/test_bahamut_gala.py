import pytest

from dlparse.enums import ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_normal_attack(transformer_atk: AttackingActionTransformer):
    # Gala Bahamut (20050525)
    # - Normal Attack AID: 10162140
    conditions = ConditionComposite()
    data = transformer_atk.transform_normal_attack_or_fs(10162140).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([1.8] * 4)
    assert combo_1.sp_gain == 5
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 4

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([9.64])
    assert combo_2.sp_gain == 5
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([6.76] * 4)
    assert combo_3.sp_gain == 5
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 4

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([18.26])
    assert combo_4.sp_gain == 15
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]
