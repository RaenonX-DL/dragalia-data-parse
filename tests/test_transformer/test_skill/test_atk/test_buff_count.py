from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.model import BuffCountBoostData
from dlparse.transformer import SkillTransformer


def test_capped(transformer_skill: SkillTransformer):
    # Lapis S2
    # https://dragalialost.gamepedia.com/Lapis
    skill_data_base = transformer_skill.transform_attacking(109502012, is_exporting=True)

    expected_data = {
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_0): BuffCountBoostData(0, 0.8, 0.05, 1319, 3, 0.2),
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_1): BuffCountBoostData(0.2, 0.8, 0.05, 1319, 2, 0.2),
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_2): BuffCountBoostData(0.4, 0.8, 0.05, 1319, 1, 0.2),
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_3): BuffCountBoostData(0.6, 0.8, 0.05, 1319, 0, 0.2),
    }
    skill_max_lv = skill_data_base.max_level

    for condition, buff_count_boost_data in expected_data.items():
        skill_data = skill_data_base.with_conditions(condition)

        # * 2 for 2 hits
        assert skill_data.buff_boost_data_mtx == [[buff_count_boost_data] * 2] * skill_max_lv


def test_uncapped(transformer_skill: SkillTransformer):
    # Karina S1
    # https://dragalialost.gamepedia.com/Karina
    skill_data = transformer_skill.transform_attacking(104402011, is_exporting=True).with_conditions()

    skill_max_lv = skill_data.max_level

    assert skill_data.buff_boost_data_mtx == [[BuffCountBoostData(0, 0, 0.05, 0, 0, 0)] * 2] * skill_max_lv
