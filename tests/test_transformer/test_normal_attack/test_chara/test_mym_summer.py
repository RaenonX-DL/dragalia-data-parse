from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_dragondrive(transformer_atk: AttackingActionTransformer):
    # Summer Mym (10950502)
    # - Mode 100: Unique Transform
    # - Unique Combo 69
    # - Action ID 901300
    conditions = ConditionComposite(Condition.SELF_SMYM_COMBO_NOT_BOOSTED)
    data = transformer_atk.transform_normal_attack(901300).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [0.66, 1.49]
    assert combo_1.sp_gain == 480
    assert combo_1.utp_gain == 150
    assert combo_1.od_rate == [1.0, 1.0]

    combo_2 = data[1]
    assert combo_2.mods == [0.66, 1.49]
    assert combo_2.sp_gain == 480
    assert combo_2.utp_gain == 150
    assert combo_2.od_rate == [1.0, 1.0]


def test_dragondrive_enhanced(transformer_atk: AttackingActionTransformer):
    # Summer Mym (10950502)
    # - Mode 100: Unique Transform
    # - Unique Combo 69
    # - Action ID 901300
    conditions = ConditionComposite(Condition.SELF_SMYM_COMBO_BOOSTED)
    data = transformer_atk.transform_normal_attack(901300).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [0.99, 2.45]
    assert combo_1.sp_gain == 480
    assert combo_1.utp_gain == 200
    assert combo_1.od_rate == [1.0, 1.0]

    combo_2 = data[1]
    assert combo_2.mods == [0.99, 2.45]
    assert combo_2.sp_gain == 480
    assert combo_2.utp_gain == 200
    assert combo_2.od_rate == [1.0, 1.0]
