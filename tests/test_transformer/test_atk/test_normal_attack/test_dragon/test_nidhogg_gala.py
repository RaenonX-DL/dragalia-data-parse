from dlparse.enums import ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_normal_attack(transformer_atk: AttackingActionTransformer):
    # Gala Reborn Nidhogg (20050524)
    # - Normal Attack AID: 10155140
    conditions = ConditionComposite()
    data = transformer_atk.transform_normal_attack_or_fs(10155140).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [4.96]
    assert combo_1.sp_gain == 5
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == [5.46]
    assert combo_2.sp_gain == 5
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == [2.08, 4.86]
    assert combo_3.sp_gain == 5
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0, 1.0]
