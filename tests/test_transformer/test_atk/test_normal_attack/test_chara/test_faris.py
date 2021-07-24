from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import AttackingActionTransformer


def test_sigil_released(transformer_atk: AttackingActionTransformer):
    # Faris (10950102)
    # - Mode 83: Sigil Released
    # - Unique Combo 62
    # - Action ID 901000
    # -------------
    # - Sigil Locked = Mode 82 = Action ID 900000 = Same as long gun
    data = transformer_atk.transform_normal_attack_or_fs(901000).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [0.97] * 5
    assert combo_1.sp_gain == 600
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 5


def test_sigil_released_target_scorchrent(transformer_atk: AttackingActionTransformer):
    # Faris (10950102)
    # - Mode 83: Sigil Released
    # - Unique Combo 62
    # - Action ID 901000
    # -------------
    # - Sigil Locked = Mode 82 = Action ID 900000 = Same as long gun
    conditions = ConditionComposite(Condition.TARGET_SCORCHRENT)
    data = transformer_atk.transform_normal_attack_or_fs(901000).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == [0.97 * 1.35] * 5
    assert combo_1.sp_gain == 600
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 5
