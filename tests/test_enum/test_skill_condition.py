import pytest

from dlparse.enums import SkillCondition, SkillConditionCheckResult, SkillConditionComposite, validate_skill_conditions
from dlparse.errors import ConditionValidationFailedError


def test_validity_result_enum():
    assert bool(SkillConditionCheckResult.PASS)
    assert not bool(SkillConditionCheckResult.MULTIPLE_HP_CONDITION)

    assert SkillConditionCheckResult.PASS.passed
    assert not SkillConditionCheckResult.MULTIPLE_BUFF_COUNT.passed


def test_validity_check():
    assert validate_skill_conditions() == SkillConditionCheckResult.PASS
    assert validate_skill_conditions([]) == SkillConditionCheckResult.PASS
    assert validate_skill_conditions(None) == SkillConditionCheckResult.PASS


def test_validity_single_hp():
    conditions = [SkillCondition.SELF_HP_1]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_hp():
    conditions = [SkillCondition.SELF_HP_1, SkillCondition.SELF_HP_FULL]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_HP_STATUS


def test_validity_single_buff():
    conditions = [SkillCondition.SELF_BUFF_10]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_buff():
    conditions = [SkillCondition.SELF_BUFF_10, SkillCondition.SELF_BUFF_25]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_BUFF_COUNT


def test_validity_single_bullet_hit_count():
    conditions = [SkillCondition.BULLET_HIT_3]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_bullet_hit_count():
    conditions = [SkillCondition.BULLET_HIT_3, SkillCondition.BULLET_HIT_8]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_BULLET_HIT


def test_validity_single_afflictions():
    conditions = [SkillCondition.TARGET_BLINDED]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_afflictions():
    conditions = [SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED]
    assert validate_skill_conditions(conditions) == SkillConditionCheckResult.PASS


def test_composite_none():
    composite = SkillConditionComposite()

    assert composite.afflictions_condition == set()
    assert composite.buff_count is None
    assert composite.bullet_hit_count is None
    assert composite.hp_condition is None


def test_composite_empty():
    composite = SkillConditionComposite(conditions=[])

    assert composite.afflictions_condition == set()
    assert composite.buff_count is None
    assert composite.bullet_hit_count is None
    assert composite.hp_condition is None


def test_composite_partial():
    composite = SkillConditionComposite(conditions=[SkillCondition.TARGET_STUNNED, SkillCondition.SELF_HP_1])

    assert composite.afflictions_condition == {SkillCondition.TARGET_STUNNED}
    assert composite.buff_count is None
    assert composite.bullet_hit_count is None
    assert composite.hp_status == SkillCondition.SELF_HP_1


def test_composite_mix():
    composite = SkillConditionComposite(conditions=[
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8, SkillCondition.SELF_BUFF_10
    ])

    assert composite.afflictions_condition == {SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED}
    assert composite.buff_count == SkillCondition.SELF_BUFF_10
    assert composite.bullet_hit_count == SkillCondition.BULLET_HIT_8
    assert composite.hp_status == SkillCondition.SELF_HP_1


def test_composite_eq():
    assert SkillConditionComposite() == SkillConditionComposite()
    assert SkillConditionComposite(SkillCondition.SELF_HP_1) == SkillConditionComposite(SkillCondition.SELF_HP_1)
    assert SkillConditionComposite(SkillCondition.SELF_HP_1) != SkillConditionComposite(SkillCondition.SELF_HP_FULL)
    assert SkillConditionComposite([SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8]) \
           == SkillConditionComposite([SkillCondition.BULLET_HIT_8, SkillCondition.SELF_HP_1])


def test_composite_add():
    assert SkillConditionComposite() + SkillConditionComposite() == SkillConditionComposite()
    assert SkillConditionComposite(SkillCondition.SELF_HP_1) == SkillConditionComposite(SkillCondition.SELF_HP_1)
    assert SkillConditionComposite(SkillCondition.SELF_HP_1) + SkillConditionComposite(SkillCondition.SELF_BUFF_10) \
           == SkillConditionComposite([SkillCondition.SELF_HP_1, SkillCondition.SELF_BUFF_10])

    with pytest.raises(ConditionValidationFailedError):
        assert SkillConditionComposite(SkillCondition.SELF_HP_1) + SkillConditionComposite(SkillCondition.SELF_HP_FULL)
