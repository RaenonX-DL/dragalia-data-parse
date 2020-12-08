import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s2(transformer_skill: SkillTransformer):
    # Meene S2
    # https://dragalialost.gamepedia.com/Meene
    skill_data_base = transformer_skill.transform_attacking(106503032)

    addl_hits = {
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_0): 0,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_1): 1,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_2): 2,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_3): 3,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_4): 4,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_5): 5,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_6): 6,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_7): 7,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_8): 8,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_9): 9,
    }

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [1 + bonus_hits, 1 + bonus_hits]
        assert skill_data.hit_count_at_max == 1 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            9 + 1.5 * bonus_hits,
            10 + 1.67 * bonus_hits
        ])
        assert skill_data.total_mod_at_max == pytest.approx(10 + 1.67 * bonus_hits)
        assert skill_data.mods == approx_matrix([
            [9.0] + [1.5] * bonus_hits,
            [10.0] + [1.67] * bonus_hits
        ])
        assert skill_data.mods_at_max == pytest.approx([10.0] + [1.67] * bonus_hits)
        assert skill_data.max_level == 2


def test_s2_6_plus_butterflies(transformer_skill: SkillTransformer):
    # Meene S2 @ 6+ butterflies
    # https://dragalialost.gamepedia.com/Meene
    skill_data_base = transformer_skill.transform_attacking(106503036)

    addl_hits = {
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_0): 0,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_1): 1,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_2): 2,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_3): 3,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_4): 4,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_5): 5,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_6): 6,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_7): 7,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_8): 8,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_9): 9,
    }

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [1 + bonus_hits, 1 + bonus_hits]
        assert skill_data.hit_count_at_max == 1 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            9 + 1.5 * bonus_hits,
            10 + 1.67 * bonus_hits
        ])
        assert skill_data.total_mod_at_max == pytest.approx(10 + 1.67 * bonus_hits)
        assert skill_data.mods == approx_matrix([
            [9.0] + [1.5] * bonus_hits,
            [10.0] + [1.67] * bonus_hits
        ])
        assert skill_data.mods_at_max == pytest.approx([10.0] + [1.67] * bonus_hits)
        assert skill_data.max_level == 2
