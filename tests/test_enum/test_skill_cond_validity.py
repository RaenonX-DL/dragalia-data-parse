from dlparse.enums import Condition, ConditionCheckResult, validate_conditions


def test_validity_result_enum():
    assert bool(ConditionCheckResult.PASS)
    assert not bool(ConditionCheckResult.MULTIPLE_HP_CONDITION)

    assert ConditionCheckResult.PASS.passed
    assert not ConditionCheckResult.MULTIPLE_BUFF_COUNT.passed


def test_validity_check():
    assert validate_conditions() == ConditionCheckResult.PASS
    assert validate_conditions([]) == ConditionCheckResult.PASS
    assert validate_conditions(None) == ConditionCheckResult.PASS


def test_validity_single_hp():
    conditions = [Condition.SELF_HP_1]
    assert validate_conditions(conditions) == ConditionCheckResult.PASS


def test_validity_multi_hp():
    conditions = [Condition.SELF_HP_1, Condition.SELF_HP_FULL]
    assert validate_conditions(conditions) == ConditionCheckResult.MULTIPLE_HP_STATUS


def test_validity_single_buff():
    conditions = [Condition.SELF_BUFF_10]
    assert validate_conditions(conditions) == ConditionCheckResult.PASS


def test_validity_multi_buff():
    conditions = [Condition.SELF_BUFF_10, Condition.SELF_BUFF_25]
    assert validate_conditions(conditions) == ConditionCheckResult.MULTIPLE_BUFF_COUNT


def test_validity_single_bullet_hit_count():
    conditions = [Condition.BULLET_HIT_3]
    assert validate_conditions(conditions) == ConditionCheckResult.PASS


def test_validity_multi_bullet_hit_count():
    conditions = [Condition.BULLET_HIT_3, Condition.BULLET_HIT_8]
    assert validate_conditions(conditions) == ConditionCheckResult.MULTIPLE_BULLET_HIT


def test_validity_single_afflictions():
    conditions = [Condition.TARGET_BLINDED]
    assert validate_conditions(conditions) == ConditionCheckResult.PASS


def test_validity_multi_afflictions():
    conditions = [Condition.TARGET_BLINDED, Condition.TARGET_STUNNED]
    assert validate_conditions(conditions) == ConditionCheckResult.PASS
