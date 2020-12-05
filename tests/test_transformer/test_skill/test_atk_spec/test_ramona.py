import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Ramona S1
    # https://dragalialost.gamepedia.com/Ramona
    skill_data_base = transformer_skill.transform_attacking(104501011)

    pre_dmg = [
        [3.05] + [2.37] * 3,
        [3.39] + [2.63] * 3,
        [3.76] + [2.93] * 3
    ]
    addl_hits = {
        SkillConditionComposite(SkillCondition.ADDL_INPUT_0): 0,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_1): 1,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_2): 2,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_3): 3,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_4): 4,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_5): 5,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_6): 6,
    }
    post_dmg = [
        [3.05],
        [3.39],
        [3.76]
    ]

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [5 + bonus_hits, 5 + bonus_hits, 5 + bonus_hits]
        assert skill_data.hit_count_at_max == 5 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            sum(pre_dmg[0]) + 2.37 * bonus_hits + sum(post_dmg[0]),
            sum(pre_dmg[1]) + 2.63 * bonus_hits + sum(post_dmg[1]),
            sum(pre_dmg[2]) + 2.93 * bonus_hits + sum(post_dmg[2]),
        ])
        assert skill_data.total_mod_at_max == pytest.approx(sum(pre_dmg[2]) + 2.93 * bonus_hits + sum(post_dmg[2]))
        assert skill_data.mods == approx_matrix([
            pre_dmg[0] + [2.37] * bonus_hits + post_dmg[0],
            pre_dmg[1] + [2.63] * bonus_hits + post_dmg[1],
            pre_dmg[2] + [2.93] * bonus_hits + post_dmg[2],
        ])
        assert skill_data.mods_at_max == pytest.approx(pre_dmg[2] + [2.93] * bonus_hits + post_dmg[2])
        assert skill_data.max_level == 3
