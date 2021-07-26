from dlparse.enums import BuffParameter, ConditionComposite, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_s1(transformer_skill: SkillTransformer):
    # Patia S1
    # https://dragalialost.wiki/w/Patia
    skill_data_base = transformer_skill.transform_supportive(105405021)

    assert skill_data_base.max_level == 4

    expected_buffs = {
        tuple(): {
            BuffEffectInfo(
                "BUF_184_ATK_LV04", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.15, 15, 0
            ),
            BuffEffectInfo(
                "BUF_184_DEF_LV04", HitTargetSimple.TEAM, BuffParameter.DEF_BUFF, 0.25, 15, 0
            ),
        },
    }

    for condition, buff_units in expected_buffs.items():
        skill_data = skill_data_base.with_conditions(ConditionComposite(condition))

        expected_buffs = buff_units
        actual_buffs = skill_data.buffs[-1]

        check_buff_unit_match(actual_buffs, expected_buffs, message=condition)
