import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_base(transformer_skill: SkillTransformer):
    # Gala Alex S1
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505021)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [3, 3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([
        1.61 * 3,
        1.80 * 3,
        2.02 * 3,
        2.02 * 3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.02 * 3)
    assert skill_data.mods == approx_matrix([
        [1.61] * 3,
        [1.80] * 3,
        [2.02] * 3,
        [2.02] * 3
    ])
    assert skill_data.mods_at_max == pytest.approx([2.02] * 3)
    assert skill_data.max_level == 4


def test_s2_base(transformer_skill: SkillTransformer):
    # Gala Alex S2
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505022)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([4.97, 5.53, 5.53])
    assert skill_data.total_mod_at_max == pytest.approx(5.53)
    assert skill_data.mods == approx_matrix([[4.97], [5.53], [5.53]])
    assert skill_data.mods_at_max == pytest.approx([5.53])
    assert skill_data.max_level == 3


def test_s1_chained(transformer_skill: SkillTransformer):
    # Gala Alex S1 @ Chained
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505023)

    # Base

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        1.61 * 3 + 3.85,
        1.80 * 3 + 4.31,
        2.02 * 3 + 4.85,
        2.02 * 3 + 4.85
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.02 * 3 + 4.85)
    assert skill_data.mods == approx_matrix([
        [1.61] * 3 + [3.85],
        [1.80] * 3 + [4.31],
        [2.02] * 3 + [4.85],
        [2.02] * 3 + [4.85]
    ])
    assert skill_data.mods_at_max == pytest.approx([2.02] * 3 + [4.85])
    assert skill_data.max_level == 4

    # DEF down

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_DEF_DOWN))

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        1.771 * 3 + 4.235,
        1.980 * 3 + 4.741,
        2.222 * 3 + 5.335,
        2.222 * 3 + 5.335
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.222 * 3 + 5.335)
    assert skill_data.mods == approx_matrix([
        [1.771] * 3 + [4.235],
        [1.980] * 3 + [4.741],
        [2.222] * 3 + [5.335],
        [2.222] * 3 + [5.335]
    ])
    assert skill_data.mods_at_max == pytest.approx([2.222] * 3 + [5.335])
    assert skill_data.max_level == 4


def test_s2_chained(transformer_skill: SkillTransformer):
    # Gala Alex S2 @ Chained
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505026)

    # Base

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        4.97 + 3.97,
        5.53 + 4.42,
        5.53 + 4.42
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.53 + 4.42)
    assert skill_data.mods == approx_matrix([
        [4.97, 3.97],
        [5.53, 4.42],
        [5.53, 4.42]
    ])
    assert skill_data.mods_at_max == pytest.approx([5.53, 4.42])
    assert skill_data.max_level == 3

    # Poisoned

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_POISONED))

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        5.467 + 4.367,
        6.083 + 4.862,
        6.083 + 4.862
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.083 + 4.862)
    assert skill_data.mods == approx_matrix([
        [5.467, 4.367],
        [6.083, 4.862],
        [6.083, 4.862]
    ])
    assert skill_data.mods_at_max == pytest.approx([6.083, 4.862])
    assert skill_data.max_level == 3


def test_s1_has_buff(transformer_skill: SkillTransformer):
    # Gala Alex S1 @ Has buff
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505024)

    # Base

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        1.61 * 3 + 3.85,
        1.80 * 3 + 4.31,
        2.02 * 3 + 4.85,
        2.02 * 3 + 4.95
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.02 * 3 + 4.95)
    assert skill_data.mods == approx_matrix([
        [1.61] * 3 + [3.85],
        [1.80] * 3 + [4.31],
        [2.02] * 3 + [4.85],
        [2.02] * 3 + [4.95]
    ])
    assert skill_data.mods_at_max == pytest.approx([2.02] * 3 + [4.95])
    assert skill_data.max_level == 4

    # DEF down

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_DEF_DOWN))

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        1.61 * 3 + 4.235,
        1.80 * 3 + 4.741,
        2.02 * 3 + 5.335,
        2.02 * 3 + 5.445
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.02 * 3 + 5.445)
    assert skill_data.mods == approx_matrix([
        [1.61] * 3 + [4.235],
        [1.80] * 3 + [4.741],
        [2.02] * 3 + [5.335],
        [2.02] * 3 + [5.445]
    ])
    assert skill_data.mods_at_max == pytest.approx([2.02] * 3 + [5.445])
    assert skill_data.max_level == 4


def test_s2_has_buff(transformer_skill: SkillTransformer):
    # Gala Alex S2 @ Has buff
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505027)

    # Base

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        4.97 + 3.97,
        5.53 + 4.42,
        5.53 + 4.52
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.53 + 4.52)
    assert skill_data.mods == approx_matrix([
        [4.97, 3.97],
        [5.53, 4.42],
        [5.53, 4.52]
    ])
    assert skill_data.mods_at_max == pytest.approx([5.53, 4.52])
    assert skill_data.max_level == 3

    # Poisoned

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_POISONED))

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        4.97 + 4.367,
        5.53 + 4.862,
        5.53 + 4.972
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.53 + 4.972)
    assert skill_data.mods == approx_matrix([
        [4.97, 4.367],
        [5.53, 4.862],
        [5.53, 4.972]
    ])
    assert skill_data.mods_at_max == pytest.approx([5.53, 4.972])
    assert skill_data.max_level == 3


def test_s1_break(transformer_skill: SkillTransformer):
    # Gala Alex S1 @ Target break
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505025)

    # Base

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        1.94 * 3 + 5.35,
        2.14 * 3 + 5.90,
        2.35 * 3 + 6.58,
        2.45 * 3 + 6.68,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.45 * 3 + 6.68)
    assert skill_data.mods == approx_matrix([
        [1.94] * 3 + [5.35],
        [2.14] * 3 + [5.90],
        [2.35] * 3 + [6.58],
        [2.45] * 3 + [6.68],
    ])
    assert skill_data.mods_at_max == pytest.approx([2.45] * 3 + [6.68])
    assert skill_data.max_level == 4

    # Target BK

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_BK_STATE))

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        2.910 * 3 + 8.025,
        3.210 * 3 + 8.850,
        3.525 * 3 + 9.870,
        3.675 * 3 + 10.02,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.675 * 3 + 10.02)
    assert skill_data.mods == approx_matrix([
        [2.910] * 3 + [8.025],
        [3.210] * 3 + [8.850],
        [3.525] * 3 + [9.870],
        [3.675] * 3 + [10.02],
    ])
    assert skill_data.mods_at_max == pytest.approx([3.675] * 3 + [10.02])
    assert skill_data.max_level == 4


def test_s2_break(transformer_skill: SkillTransformer):
    # Gala Alex S2 @ Target break
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data_base = transformer_skill.transform_attacking(101505028)

    # Base

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        5.93 * 2,
        6.48 * 2,
        6.58 * 2,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.58 * 2)
    assert skill_data.mods == approx_matrix([
        [5.93] * 2,
        [6.48] * 2,
        [6.58] * 2,
    ])
    assert skill_data.mods_at_max == pytest.approx([6.58] * 2)
    assert skill_data.max_level == 3

    # Target BK

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_BK_STATE))

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        8.895 * 2,
        9.720 * 2,
        9.870 * 2,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(9.870 * 2)
    assert skill_data.mods == approx_matrix([
        [8.895] * 2,
        [9.720] * 2,
        [9.870] * 2,
    ])
    assert skill_data.mods_at_max == pytest.approx([9.870] * 2)
    assert skill_data.max_level == 3
