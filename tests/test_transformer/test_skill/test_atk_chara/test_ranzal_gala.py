import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_no_chara_ability(transformer_skill: SkillTransformer):
    # Gala Ranzal S1
    # https://dragalialost.gamepedia.com/Gala_Ranzal
    skill_data_base = transformer_skill.transform_attacking(101503011)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [6, 6, 6]
    assert skill_data.hit_count_at_max == 6
    assert skill_data.total_mod == pytest.approx([
        2.464 * 6,
        2.728 * 6,
        3.036 * 6
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.036 * 6)
    assert skill_data.mods == approx_matrix([
        [2.464] * 6,
        [2.728] * 6,
        [3.036] * 6
    ])
    assert skill_data.mods_at_max == pytest.approx([3.036] * 6)
    assert skill_data.max_level == 3


def test_s1_has_chara_ability(transformer_skill: SkillTransformer):
    # Gala Ranzal S1
    # https://dragalialost.gamepedia.com/Gala_Ranzal
    skill_data_base = transformer_skill.transform_attacking(101503011, ability_ids=[124])

    dmg_up_rate = {
        SkillConditionComposite(SkillCondition.SELF_GAUGE_FILLED_0): 1,
        SkillConditionComposite(SkillCondition.SELF_GAUGE_FILLED_1): 1.2,
        SkillConditionComposite(SkillCondition.SELF_GAUGE_FILLED_2): 2,
    }

    for cond_comp, up_rate in dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [6, 6, 6]
        assert skill_data.hit_count_at_max == 6
        assert skill_data.total_mod == pytest.approx([
            2.464 * 6 * up_rate,
            2.728 * 6 * up_rate,
            3.036 * 6 * up_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(3.036 * up_rate * 6)
        assert skill_data.mods == approx_matrix([
            [2.464 * up_rate] * 6,
            [2.728 * up_rate] * 6,
            [3.036 * up_rate] * 6
        ])
        assert skill_data.mods_at_max == pytest.approx([3.036 * up_rate] * 6)
        assert skill_data.max_level == 3
