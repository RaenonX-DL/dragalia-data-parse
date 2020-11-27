import pytest

from dlparse.enums import (
    Affliction, SkillCondition, SkillConditionCategories as CondCat, SkillConditionMaxCount as CondMax
)
from dlparse.errors import EnumConversionError


def test_member_contains():
    assert SkillCondition.TARGET_PARALYZED in CondCat.target_affliction
    assert SkillCondition.BULLET_HIT_1 not in CondCat.target_affliction

    assert SkillCondition.SELF_BUFF_10 in CondCat.self_buff_count
    assert SkillCondition.BULLET_HIT_1 not in CondCat.self_buff_count


def test_conversion():
    assert CondCat.target_affliction.convert(SkillCondition.TARGET_PARALYZED) == Affliction.PARALYZE
    with pytest.raises(EnumConversionError):
        CondCat.target_affliction.convert(SkillCondition.BULLET_HIT_1)

    assert CondCat.self_buff_count.convert(SkillCondition.SELF_BUFF_10) == 10
    with pytest.raises(EnumConversionError):
        CondCat.target_affliction.convert(SkillCondition.BULLET_HIT_1)


def test_reverse_conversion():
    assert CondCat.target_affliction.convert_reversed(Affliction.PARALYZE) == SkillCondition.TARGET_PARALYZED
    with pytest.raises(EnumConversionError):
        CondCat.target_affliction.convert_reversed(SkillCondition.BULLET_HIT_1)

    assert CondCat.self_buff_count.convert_reversed(10) == SkillCondition.SELF_BUFF_10
    with pytest.raises(EnumConversionError):
        CondCat.self_buff_count.convert_reversed(SkillCondition.BULLET_HIT_1)


def test_get_members():
    assert CondCat.target_affliction.members == {
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
        SkillCondition.TARGET_CRASHWINDED,
        SkillCondition.TARGET_SHADOWBLIGHTED,
    }


def test_max_allowed_count():
    assert CondCat.target_affliction.max_count_allowed == CondMax.MULTIPLE
    assert CondCat.self_buff_count.max_count_allowed == CondMax.SINGLE


def test_extract():
    conditions = [
        SkillCondition.TARGET_PARALYZED,
        SkillCondition.TARGET_STUNNED,
        SkillCondition.SELF_BUFF_10,
        SkillCondition.BULLET_HIT_1
    ]

    assert CondCat.target_affliction.extract(conditions) == \
           {SkillCondition.TARGET_PARALYZED, SkillCondition.TARGET_STUNNED}
    assert CondCat.self_buff_count.extract(conditions) == SkillCondition.SELF_BUFF_10

    condition = [SkillCondition.TARGET_POISONED]

    assert CondCat.target_affliction.extract(condition) == {SkillCondition.TARGET_POISONED}
    assert CondCat.target_affliction.extract([SkillCondition.BULLET_HIT_1]) == set()