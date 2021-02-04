from dlparse.enums import BuffParameter, Condition, ConditionComposite, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_sup_nadine_s1(transformer_skill: SkillTransformer):
    # Nadine S1
    # https://dragalialost.wiki/w/Nadine
    skill_data_base = transformer_skill.transform_supportive(105501021)

    assert skill_data_base.max_level == 3

    expected_buffs = {
        (Condition.COVER_TEAMMATE_0,): set(),
        (Condition.COVER_TEAMMATE_1,): {
            BuffEffectInfo(
                "LAN_127_04_1_TENSION_LV03", HitTargetSimple.SELF, BuffParameter.ENERGY_LEVEL, 1, 0, 1
            ),
        },
        (Condition.COVER_TEAMMATE_2,): {
            BuffEffectInfo(
                "LAN_127_04_2_TENSION_LV03", HitTargetSimple.SELF, BuffParameter.ENERGY_LEVEL, 3, 0, 1
            ),
        },
        (Condition.COVER_TEAMMATE_3,): {
            BuffEffectInfo(
                "LAN_127_04_2_TENSION_LV03", HitTargetSimple.SELF, BuffParameter.ENERGY_LEVEL, 3, 0, 1
            ),
        },
    }

    for condition, buff_units in expected_buffs.items():
        skill_data = skill_data_base.with_conditions(ConditionComposite(condition))

        expected_buffs = buff_units
        actual_buffs = skill_data.buffs[-1]

        check_buff_unit_match(actual_buffs, expected_buffs, message=condition)
