import pytest

from dlparse.enums import (
    SkillCondition, SkillConditionCategories as CondCat, SkillConditionMaxCount as CondMax, Status,
)
from dlparse.errors import EnumConversionError


def test_member_contains():
    assert SkillCondition.TARGET_PARALYZED in CondCat.target_status
    assert SkillCondition.BULLET_HIT_1 not in CondCat.target_status

    assert SkillCondition.SELF_BUFF_10 in CondCat.self_buff_count
    assert SkillCondition.BULLET_HIT_1 not in CondCat.self_buff_count


def test_conversion():
    assert CondCat.target_status.convert(SkillCondition.TARGET_PARALYZED) == Status.PARALYZE
    with pytest.raises(EnumConversionError):
        CondCat.target_status.convert(SkillCondition.BULLET_HIT_1)

    assert CondCat.self_buff_count.convert(SkillCondition.SELF_BUFF_10) == 10
    with pytest.raises(EnumConversionError):
        CondCat.target_status.convert(SkillCondition.BULLET_HIT_1)


def test_reverse_conversion():
    assert CondCat.target_status.convert_reversed(Status.PARALYZE) == SkillCondition.TARGET_PARALYZED
    with pytest.raises(EnumConversionError):
        CondCat.target_status.convert_reversed(SkillCondition.BULLET_HIT_1)

    assert CondCat.self_buff_count.convert_reversed(10) == SkillCondition.SELF_BUFF_10
    with pytest.raises(EnumConversionError):
        CondCat.self_buff_count.convert_reversed(SkillCondition.BULLET_HIT_1)


def test_get_members():
    assert CondCat.target_status.members == {
        SkillCondition.TARGET_POISONED,
        SkillCondition.TARGET_BURNED,
        SkillCondition.TARGET_FROZEN,
        SkillCondition.TARGET_PARALYZED,
        SkillCondition.TARGET_BLINDED,
        SkillCondition.TARGET_STUNNED,
        SkillCondition.TARGET_CURSED,
        SkillCondition.TARGET_BOGGED,
        SkillCondition.TARGET_SLEPT,
        SkillCondition.TARGET_FROSTBITTEN,
        SkillCondition.TARGET_FLASHBURNED,
        SkillCondition.TARGET_STORMLASHED,
        SkillCondition.TARGET_SHADOWBLIGHTED,
        SkillCondition.TARGET_AFFLICTED,
        SkillCondition.TARGET_DEF_DOWN,
        SkillCondition.TARGET_BUFFED,
        SkillCondition.TARGET_DEBUFFED,
        SkillCondition.TARGET_BK_STATE
    }


def test_max_allowed_count():
    assert CondCat.target_status.max_count_allowed == CondMax.MULTIPLE
    assert CondCat.self_buff_count.max_count_allowed == CondMax.SINGLE


def test_extract():
    conditions = [
        SkillCondition.TARGET_PARALYZED,
        SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_BUFF_10,
        SkillCondition.BULLET_HIT_1
    ]

    assert CondCat.target_status.extract(conditions) == \
           {SkillCondition.TARGET_PARALYZED, SkillCondition.TARGET_STUNNED}
    assert CondCat.self_buff_count.extract(conditions) == SkillCondition.SELF_BUFF_10

    condition = [SkillCondition.TARGET_POISONED]

    assert CondCat.target_status.extract(condition) == {SkillCondition.TARGET_POISONED}
    assert CondCat.target_status.extract([SkillCondition.BULLET_HIT_1]) == set()
