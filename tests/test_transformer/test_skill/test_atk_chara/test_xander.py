import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_p2(transformer_skill: SkillTransformer):
    # Xander S1 P2
    # https://dragalialost.wiki/w/Xander
    skill_data_base = transformer_skill.transform_attacking(101502013)

    condition_to_dmg_up_rate = {
        (Condition.SELF_BUFF_0,): 1 + 0,
        (Condition.SELF_BUFF_10,): 1 + 0.05 * 10,
        (Condition.SELF_BUFF_15,): 1 + 0.05 * 15,
        (Condition.SELF_BUFF_20,): 1 + 0.05 * 20,
        (Condition.SELF_BUFF_25,): 1 + 0.05 * 25,
        (Condition.SELF_BUFF_30,): 1 + 0.05 * 30,
        (Condition.SELF_BUFF_35,): 1 + 0.05 * 35,
        (Condition.SELF_BUFF_40,): 1 + 0.05 * 40,
        (Condition.SELF_BUFF_45,): 1 + 0.05 * 45,
        (Condition.SELF_BUFF_50,): 1 + 0.05 * 50,
    }

    for conditions, boost_rate in condition_to_dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(ConditionComposite(conditions))

        assert skill_data.hit_count == [0, 0, 0, 1]
        assert skill_data.hit_count_at_max == 1
        assert skill_data.total_mod == pytest.approx([0, 0, 0, 16.74 * boost_rate])
        assert skill_data.total_mod_at_max == pytest.approx(16.74 * boost_rate)
        assert skill_data.mods == approx_matrix([[], [], [], [16.74 * boost_rate]])
        assert skill_data.mods_at_max == pytest.approx([16.74 * boost_rate])
        assert skill_data.max_level == 4


def test_s1_p3(transformer_skill: SkillTransformer):
    # Xander S1 P3
    # https://dragalialost.wiki/w/Xander
    skill_data_base = transformer_skill.transform_attacking(101502014)

    condition_to_dmg_up_rate = {
        (Condition.SELF_BUFF_0,): 1 + 0,
        (Condition.SELF_BUFF_10,): 1 + 0.05 * 10,
        (Condition.SELF_BUFF_15,): 1 + 0.05 * 15,
        (Condition.SELF_BUFF_20,): 1 + 0.05 * 20,
        (Condition.SELF_BUFF_25,): 1 + 0.05 * 25,
        (Condition.SELF_BUFF_30,): 1 + 0.05 * 30,
        (Condition.SELF_BUFF_35,): 1 + 0.05 * 35,
        (Condition.SELF_BUFF_40,): 1 + 0.05 * 40,
        (Condition.SELF_BUFF_45,): 1 + 0.05 * 45,
        (Condition.SELF_BUFF_50,): 1 + 0.05 * 50,
    }

    for conditions, boost_rate in condition_to_dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(ConditionComposite(conditions))

        assert skill_data.hit_count == [0, 0, 0, 1]
        assert skill_data.hit_count_at_max == 1
        assert skill_data.total_mod == pytest.approx([0, 0, 0, 16.8 * boost_rate])
        assert skill_data.total_mod_at_max == pytest.approx(16.8 * boost_rate)
        assert skill_data.mods == approx_matrix([[], [], [], [16.8 * boost_rate]])
        assert skill_data.mods_at_max == pytest.approx([16.8 * boost_rate])
        assert skill_data.max_level == 4
