from dlparse.enums import SkillCondition, SkillConditionCheckResult


def test_validity_result_enum():
    assert bool(SkillConditionCheckResult.PASS)
    assert not bool(SkillConditionCheckResult.MULTIPLE_HP)

    assert SkillConditionCheckResult.PASS.passed
    assert not SkillConditionCheckResult.MULTIPLE_BUFF.passed


def test_validity_check():
    assert SkillCondition.validate_conditions() == SkillConditionCheckResult.PASS
    assert SkillCondition.validate_conditions([]) == SkillConditionCheckResult.PASS
    assert SkillCondition.validate_conditions(None) == SkillConditionCheckResult.PASS


def test_validity_multi_hp():
    conditions = [SkillCondition.SELF_HP_1, SkillCondition.SELF_HP_FULL]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_HP


def test_validity_multi_buff():
    conditions = [SkillCondition.SELF_BUFF_10, SkillCondition.SELF_BUFF_25]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_BUFF


def test_validity_multi_afflictions():
    conditions = [SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.PASS
