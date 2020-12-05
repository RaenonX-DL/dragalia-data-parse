import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s2(transformer_skill: SkillTransformer):
    # Meene S2
    # https://dragalialost.gamepedia.com/Meene
    skill_data_base = transformer_skill.transform_attacking(106503032)

    # TEST: TBA - Meene S2 conditional affliction (poison)

    addl_dmg = {
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_0): 1.67 * 0,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_1): 1.67 * 1,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_2): 1.67 * 2,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_3): 1.67 * 3,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_4): 1.67 * 4,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_5): 1.67 * 5,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_6): 1.67 * 6,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_7): 1.67 * 7,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_8): 1.67 * 8,
        SkillConditionComposite(SkillCondition.BULLETS_ON_MAP_9): 1.67 * 9,
    }

    for cond_comp, dmg_up in addl_dmg.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        extra_hits = cond_comp.bullets_on_map_converted

        assert skill_data.hit_count == [1 + extra_hits, 1 + extra_hits]
        assert skill_data.hit_count_at_max == 1 + extra_hits
        assert skill_data.total_mod == pytest.approx([
            9 + 1.5 * extra_hits,
            10 + 1.67 * extra_hits
        ])
        assert skill_data.total_mod_at_max == pytest.approx(10 + 1.67 * extra_hits)
        assert skill_data.mods == approx_matrix([
            [9.0] + [1.5] * extra_hits,
            [10.0] + [1.67] * extra_hits
        ])
        assert skill_data.mods_at_max == pytest.approx([10.0] + [1.67] * extra_hits)
        assert skill_data.max_level == 2
