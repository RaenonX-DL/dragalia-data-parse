from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_dragondrive(transformer_atk: AttackingActionTransformer):
    # Summer Mym (10950502)
    # - Mode 100: Unique Transform
    # - Unique Combo 69
    # - Action ID 901300
    normal_attack_data = transformer_atk.transform_normal_attack(901300)

    combo_1 = normal_attack_data.combos[0].combo_info[ConditionComposite(Condition.SELF_COMBO_NOT_BOOSTED)]
    assert combo_1.mods == [0.66, 1.49]
    assert combo_1.sp_gain == 480
    assert combo_1.utp_gain == 150
    assert combo_1.od_rate == [1.0, 1.0]

    combo_2 = normal_attack_data.combos[1].combo_info[ConditionComposite(Condition.SELF_COMBO_NOT_BOOSTED)]
    assert combo_2.mods == [0.66, 1.49]
    assert combo_2.sp_gain == 480
    assert combo_2.utp_gain == 150
    assert combo_2.od_rate == [1.0, 1.0]


def test_dragondrive_enhanced(transformer_atk: AttackingActionTransformer):
    # Summer Mym (10950502)
    # - Mode 100: Unique Transform
    # - Unique Combo 69
    # - Action ID 901300
    normal_attack_data = transformer_atk.transform_normal_attack(901300)

    combo_1 = normal_attack_data.combos[0].combo_info[ConditionComposite(Condition.SELF_COMBO_BOOSTED)]
    assert combo_1.mods == [0.99, 2.45]
    assert combo_1.sp_gain == 480
    assert combo_1.utp_gain == 200
    assert combo_1.od_rate == [1.0, 1.0]

    combo_2 = normal_attack_data.combos[1].combo_info[ConditionComposite(Condition.SELF_COMBO_BOOSTED)]
    assert combo_2.mods == [0.99, 2.45]
    assert combo_2.sp_gain == 480
    assert combo_2.utp_gain == 200
    assert combo_2.od_rate == [1.0, 1.0]
