from dlparse.enums import ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_normal_attack(transformer_atk: AttackingActionTransformer):
    # Tiki in Divine Dragon (10350203 - 29900006)
    # - Normal Attack AID: 10093140
    conditions = ConditionComposite()
    data = transformer_atk.transform_normal_attack(10093140).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [3.17]
    assert combo_1.sp_gain == 290
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == [3.78]
    assert combo_2.sp_gain == 350
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == [5.37]
    assert combo_3.sp_gain == 520
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0]
