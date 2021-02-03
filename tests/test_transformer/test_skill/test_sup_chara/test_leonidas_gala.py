from dlparse.enums import BuffParameter, Condition, ConditionComposite, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_s2(transformer_skill: SkillTransformer):
    # Gala Leonidas S2
    # https://dragalialost.wiki/w/Gala_Leonidas
    skill_data_base = transformer_skill.transform_supportive(109501012)

    assert skill_data_base.max_level == 2

    expected_buffs = {
        (Condition.ACTION_COND_LV_1,): [
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.1, 40, 0
                ),
            },
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.1, 40, 0
                ),
            }
        ],
        (Condition.ACTION_COND_LV_2,): [
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.1, 40, 0
                ),
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.05, 40, 0
                ),
            },
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.1, 40, 0
                ),
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.05, 40, 0
                ),
            }
        ],
        (Condition.ACTION_COND_LV_3,): [
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.15, 40, 0
                ),
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.05, 40, 0
                ),
            },
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.15, 40, 0
                ),
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.05, 40, 0
                ),
            }
        ],
        (Condition.ACTION_COND_LV_4,): [
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.2, 40, 0
                ),
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.1, 40, 0
                ),
            },
            {
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.2, 40, 0
                ),
                BuffEffectInfo(
                    "GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.1, 40, 0
                ),
            }
        ],
        (Condition.ACTION_COND_LV_5,): [
            {
                BuffEffectInfo("GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.2, 0, 0),
                BuffEffectInfo("GUN_107_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.1, 0, 0),
            },
            {
                BuffEffectInfo("GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.DAMAGE_REDUCTION, 0.2, 0, 0),
                BuffEffectInfo("GUN_107_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.1, 0, 0),
            }
        ],
    }

    for condition, buff_units in expected_buffs.items():
        skill_data = skill_data_base.with_conditions(ConditionComposite(condition))

        check_buff_unit_match(skill_data.max_lv_buffs, buff_units[skill_data.max_level - 1], message=condition)

        for skill_lv in range(skill_data_base.max_level):
            expected_buffs = buff_units[skill_lv]
            actual_buffs = skill_data.buffs[skill_lv]

            check_buff_unit_match(actual_buffs, expected_buffs, message=condition)
