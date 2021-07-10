from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_possible_conditions_is_sorted_gmascula(transformer_atk: AttackingActionTransformer):
    # Gala Mascula (10250203)
    # - Mode 94: S2 Effective
    # - Unique Combo 66
    # - Action ID 202800
    data = transformer_atk.transform_normal_attack(202800)

    assert data.possible_conditions == [ConditionComposite(), ConditionComposite(Condition.SELF_GMASCULA_S1_LV3)]


def test_possible_conditions_is_sorted_smym(transformer_atk: AttackingActionTransformer):
    # Summer Mym (10950502)
    # - Mode 100: Unique Transform
    # - Unique Combo 69
    # - Action ID 901300
    data = transformer_atk.transform_normal_attack(901300)

    assert data.possible_conditions == [
        ConditionComposite(Condition.SELF_SMYM_COMBO_NOT_BOOSTED),
        ConditionComposite(Condition.SELF_SMYM_COMBO_BOOSTED)
    ]
