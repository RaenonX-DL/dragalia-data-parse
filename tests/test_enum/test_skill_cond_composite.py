import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.errors import ConditionValidationFailedError


def test_composite_none():
    composite = ConditionComposite()

    assert composite.afflictions_condition == set()
    assert composite.buff_count is None
    assert composite.bullet_hit_count is None
    assert composite.hp_condition is None


def test_composite_empty():
    composite = ConditionComposite(conditions=[])

    assert composite.afflictions_condition == set()
    assert composite.buff_count is None
    assert composite.bullet_hit_count is None
    assert composite.hp_condition is None


def test_composite_partial():
    composite = ConditionComposite(conditions=[Condition.TARGET_STUNNED, Condition.SELF_HP_1])

    assert composite.afflictions_condition == {Condition.TARGET_STUNNED}
    assert composite.buff_count is None
    assert composite.bullet_hit_count is None
    assert composite.hp_status == Condition.SELF_HP_1


def test_composite_mix():
    composite = ConditionComposite(conditions=[
        Condition.TARGET_BLINDED, Condition.TARGET_STUNNED,
        Condition.SELF_HP_1, Condition.BULLET_HIT_8, Condition.SELF_BUFF_10
    ])

    assert composite.afflictions_condition == {Condition.TARGET_BLINDED, Condition.TARGET_STUNNED}
    assert composite.buff_count == Condition.SELF_BUFF_10
    assert composite.bullet_hit_count == Condition.BULLET_HIT_8
    assert composite.hp_status == Condition.SELF_HP_1


def test_composite_eq():
    assert ConditionComposite() == ConditionComposite()
    assert ConditionComposite(Condition.SELF_HP_1) == ConditionComposite(Condition.SELF_HP_1)
    assert ConditionComposite(Condition.SELF_HP_1) != ConditionComposite(Condition.SELF_HP_FULL)
    assert ConditionComposite([Condition.SELF_HP_1, Condition.BULLET_HIT_8]) \
           == ConditionComposite([Condition.BULLET_HIT_8, Condition.SELF_HP_1])


def test_composite_add():
    assert ConditionComposite() + ConditionComposite() == ConditionComposite()
    assert ConditionComposite(Condition.SELF_HP_1) == ConditionComposite(Condition.SELF_HP_1)
    assert ConditionComposite(Condition.SELF_HP_1) + ConditionComposite(Condition.SELF_BUFF_10) \
           == ConditionComposite([Condition.SELF_HP_1, Condition.SELF_BUFF_10])

    with pytest.raises(ConditionValidationFailedError):
        assert ConditionComposite(Condition.SELF_HP_1) + ConditionComposite(Condition.SELF_HP_FULL)


def test_composite_def_down_sorted():
    cond_comp = ConditionComposite(Condition.TARGET_DEF_DOWN)
    assert cond_comp.conditions_sorted == (Condition.TARGET_DEF_DOWN,)

    cond_comp = ConditionComposite([Condition.TARGET_PARALYZED, Condition.TARGET_DEF_DOWN])
    assert cond_comp.conditions_sorted == (Condition.TARGET_PARALYZED, Condition.TARGET_DEF_DOWN)
