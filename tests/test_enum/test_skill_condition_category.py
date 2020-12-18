import pytest

from dlparse.enums import (
    Condition, ConditionCategories as CondCat, ConditionMaxCount as CondMax, Status,
)
from dlparse.errors import EnumConversionError


def test_member_contains():
    assert Condition.TARGET_PARALYZED in CondCat.target_status
    assert Condition.BULLET_HIT_1 not in CondCat.target_status

    assert Condition.SELF_BUFF_10 in CondCat.self_buff_count
    assert Condition.BULLET_HIT_1 not in CondCat.self_buff_count


def test_conversion():
    assert CondCat.target_status.convert(Condition.TARGET_PARALYZED) == Status.PARALYZE
    with pytest.raises(EnumConversionError):
        CondCat.target_status.convert(Condition.BULLET_HIT_1)

    assert CondCat.self_buff_count.convert(Condition.SELF_BUFF_10) == 10
    with pytest.raises(EnumConversionError):
        CondCat.target_status.convert(Condition.BULLET_HIT_1)


def test_reverse_conversion():
    assert CondCat.target_status.convert_reversed(Status.PARALYZE) == Condition.TARGET_PARALYZED
    with pytest.raises(EnumConversionError):
        CondCat.target_status.convert_reversed(Condition.BULLET_HIT_1)

    assert CondCat.self_buff_count.convert_reversed(10) == Condition.SELF_BUFF_10
    with pytest.raises(EnumConversionError):
        CondCat.self_buff_count.convert_reversed(Condition.BULLET_HIT_1)


def test_get_members():
    assert CondCat.target_status.members == {
        Condition.TARGET_POISONED,
        Condition.TARGET_BURNED,
        Condition.TARGET_FROZEN,
        Condition.TARGET_PARALYZED,
        Condition.TARGET_BLINDED,
        Condition.TARGET_STUNNED,
        Condition.TARGET_CURSED,
        Condition.TARGET_BOGGED,
        Condition.TARGET_SLEPT,
        Condition.TARGET_FROSTBITTEN,
        Condition.TARGET_FLASHBURNED,
        Condition.TARGET_STORMLASHED,
        Condition.TARGET_SHADOWBLIGHTED,
        Condition.TARGET_AFFLICTED,
        Condition.TARGET_DEF_DOWN,
        Condition.TARGET_BUFFED,
        Condition.TARGET_DEBUFFED,
        Condition.TARGET_BK_STATE
    }


def test_max_allowed_count():
    assert CondCat.target_status.max_count_allowed == CondMax.MULTIPLE
    assert CondCat.self_buff_count.max_count_allowed == CondMax.SINGLE


def test_extract():
    conditions = [
        Condition.TARGET_PARALYZED,
        Condition.TARGET_STUNNED,
        Condition.SELF_BUFF_10,
        Condition.BULLET_HIT_1
    ]

    assert CondCat.target_status.extract(conditions) == \
           {Condition.TARGET_PARALYZED, Condition.TARGET_STUNNED}
    assert CondCat.self_buff_count.extract(conditions) == Condition.SELF_BUFF_10

    condition = [Condition.TARGET_POISONED]

    assert CondCat.target_status.extract(condition) == {Condition.TARGET_POISONED}
    assert CondCat.target_status.extract([Condition.BULLET_HIT_1]) == set()
