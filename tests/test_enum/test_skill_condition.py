from dlparse.enums import SkillCondition, SkillConditionCheckResult, SkillConditionComposite


def test_validity_result_enum():
    assert bool(SkillConditionCheckResult.PASS)
    assert not bool(SkillConditionCheckResult.MULTIPLE_HP)

    assert SkillConditionCheckResult.PASS.passed
    assert not SkillConditionCheckResult.MULTIPLE_BUFF.passed


def test_validity_check():
    assert SkillCondition.validate_conditions() == SkillConditionCheckResult.PASS
    assert SkillCondition.validate_conditions([]) == SkillConditionCheckResult.PASS
    assert SkillCondition.validate_conditions(None) == SkillConditionCheckResult.PASS


def test_validity_single_hp():
    conditions = [SkillCondition.SELF_HP_1]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_hp():
    conditions = [SkillCondition.SELF_HP_1, SkillCondition.SELF_HP_FULL]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_HP


def test_validity_single_buff():
    conditions = [SkillCondition.SELF_BUFF_10]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_buff():
    conditions = [SkillCondition.SELF_BUFF_10, SkillCondition.SELF_BUFF_25]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_BUFF


def test_validity_single_bullet_hit_count():
    conditions = [SkillCondition.BULLET_HIT_3]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_bullet_hit_count():
    conditions = [SkillCondition.BULLET_HIT_3, SkillCondition.BULLET_HIT_8]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.MULTIPLE_BULLET_HIT


def test_validity_single_afflictions():
    conditions = [SkillCondition.TARGET_BLINDED]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.PASS


def test_validity_multi_afflictions():
    conditions = [SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED]
    assert SkillCondition.validate_conditions(conditions) == SkillConditionCheckResult.PASS


def test_extract_afflictions():
    # Empty condition
    assert SkillCondition.extract_afflictions([]) == set()

    # Included without any other conditions
    conditions = [SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED]
    assert SkillCondition.extract_afflictions(conditions) == {
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED
    }

    # Not included except the other conditions
    conditions = [SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8]
    assert SkillCondition.extract_afflictions(conditions) == set()

    # Mixed
    conditions = [
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8
    ]
    assert SkillCondition.extract_afflictions(conditions) == {
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED
    }


def test_extract_buff_count():
    # Empty condition
    assert SkillCondition.extract_buff_count([]) is None

    # Included without any other conditions
    assert SkillCondition.extract_buff_count([SkillCondition.SELF_BUFF_10]) == SkillCondition.SELF_BUFF_10

    # Not included except the other conditions
    conditions = [SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8]
    assert SkillCondition.extract_buff_count(conditions) is None

    # Mixed
    conditions = [
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8, SkillCondition.SELF_BUFF_10
    ]
    assert SkillCondition.extract_buff_count(conditions) == SkillCondition.SELF_BUFF_10


def test_extract_bullet_hit_count():
    # Empty condition
    assert SkillCondition.extract_bullet_hit_count([]) is None

    # Included without any other conditions
    assert SkillCondition.extract_bullet_hit_count([SkillCondition.BULLET_HIT_8]) == SkillCondition.BULLET_HIT_8

    # Not included except the other conditions
    conditions = [SkillCondition.SELF_HP_1, SkillCondition.SELF_BUFF_10]
    assert SkillCondition.extract_bullet_hit_count(conditions) is None

    # Mixed
    conditions = [
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8, SkillCondition.SELF_BUFF_10
    ]
    assert SkillCondition.extract_bullet_hit_count(conditions) == SkillCondition.BULLET_HIT_8


def test_extract_hp_condition():
    # Empty condition
    assert SkillCondition.extract_hp_condition([]) is None

    # Included without any other conditions
    assert SkillCondition.extract_hp_condition([SkillCondition.SELF_HP_1]) == SkillCondition.SELF_HP_1

    # Not included except the other conditions
    conditions = [SkillCondition.BULLET_HIT_8, SkillCondition.SELF_BUFF_10]
    assert SkillCondition.extract_hp_condition(conditions) is None

    # Mixed
    conditions = [
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8, SkillCondition.SELF_BUFF_10
    ]
    assert SkillCondition.extract_hp_condition(conditions) == SkillCondition.SELF_HP_1


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
    assert composite.hp_condition == SkillCondition.SELF_HP_1


def test_composite_mix():
    composite = SkillConditionComposite(conditions=[
        SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8, SkillCondition.SELF_BUFF_10
    ])

    assert composite.afflictions_condition == {SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_STUNNED}
    assert composite.buff_count == SkillCondition.SELF_BUFF_10
    assert composite.bullet_hit_count == SkillCondition.BULLET_HIT_8
    assert composite.hp_condition == SkillCondition.SELF_HP_1


def test_composite_eq():
    assert SkillConditionComposite() == SkillConditionComposite()
    assert SkillConditionComposite(SkillCondition.SELF_HP_1) == SkillConditionComposite(SkillCondition.SELF_HP_1)
    assert SkillConditionComposite(SkillCondition.SELF_HP_1) != SkillConditionComposite(SkillCondition.SELF_HP_FULL)
    assert SkillConditionComposite([SkillCondition.SELF_HP_1, SkillCondition.BULLET_HIT_8]) \
           == SkillConditionComposite([SkillCondition.BULLET_HIT_8, SkillCondition.SELF_HP_1])
