import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Lathna S1
    # https://dragalialost.gamepedia.com/Lathna
    skill_data_base = transformer_skill.transform_attacking(105505021)

    pre_dmg = [
        [1.79] * 3,
        [1.99] * 3,
        [2.21] * 3,
        [2.61] * 3,
    ]
    addl_hits = {
        SkillConditionComposite(SkillCondition.ADDL_INPUT_0): 0,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_1): 1,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_2): 2,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_3): 3,
        SkillConditionComposite(SkillCondition.ADDL_INPUT_4): 4,
    }
    post_dmg = [
        [1.79],
        [1.99],
        [2.21],
        [2.61]
    ]

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [4 + bonus_hits, 4 + bonus_hits, 4 + bonus_hits, 4 + bonus_hits]
        assert skill_data.hit_count_at_max == 4 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            sum(pre_dmg[0]) + 1.79 * bonus_hits + sum(post_dmg[0]),
            sum(pre_dmg[1]) + 1.99 * bonus_hits + sum(post_dmg[1]),
            sum(pre_dmg[2]) + 2.21 * bonus_hits + sum(post_dmg[2]),
            sum(pre_dmg[3]) + 2.61 * bonus_hits + sum(post_dmg[3]),
        ])
        assert skill_data.total_mod_at_max == pytest.approx(sum(pre_dmg[3]) + 2.61 * bonus_hits + sum(post_dmg[3]))
        assert skill_data.mods == approx_matrix([
            pre_dmg[0] + [1.79] * bonus_hits + post_dmg[0],
            pre_dmg[1] + [1.99] * bonus_hits + post_dmg[1],
            pre_dmg[2] + [2.21] * bonus_hits + post_dmg[2],
            pre_dmg[3] + [2.61] * bonus_hits + post_dmg[3],
        ])
        assert skill_data.mods_at_max == pytest.approx(pre_dmg[3] + [2.61] * bonus_hits + post_dmg[3])
        assert skill_data.max_level == 4
