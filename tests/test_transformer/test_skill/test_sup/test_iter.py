from dlparse.enums import BuffParameter, Condition, ConditionComposite, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_no_condition(transformer_skill: SkillTransformer):
    # Kirsty S2
    # https://dragalialost.gamepedia.com/Kirsty
    skill_data = transformer_skill.transform_supportive(105503022)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buffs_lv_max = {
        ConditionComposite(): {
            BuffEffectInfo("BUF_ALL_ATK_SSR_30_LV03", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.25, 15, 0)
        },
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        check_buff_unit_match(
            entry.max_lv_buffs, expected_buffs_lv_max[entry.condition_comp], message=entry.condition_comp
        )

        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"


def test_element_restricted(transformer_skill: SkillTransformer):
    # Emma S1
    # https://dragalialost.gamepedia.com/Emma
    skill_data = transformer_skill.transform_supportive(105401031)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buffs_lv_max = {
        ConditionComposite(Condition.TARGET_FLAME): {
            BuffEffectInfo("BUF_160_ATK_FIRE_LV03", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.25, 15, 0)
        },
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        check_buff_unit_match(
            entry.max_lv_buffs, expected_buffs_lv_max[entry.condition_comp], message=entry.condition_comp
        )
        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"


def test_teammate_coverage(transformer_skill: SkillTransformer):
    # Summer Cleo S2
    # https://dragalialost.gamepedia.com/Summer_Cleo
    skill_data = transformer_skill.transform_supportive(106504012)

    possible_entries = skill_data.get_all_possible_entries()

    base_buffs_at_max = {
        BuffEffectInfo("BOW_108_04_ATK_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK_BUFF, 0.05, 10, 0),
        BuffEffectInfo("BOW_108_04_CRT_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE_BUFF, 0.03, 10,
                       0),
        BuffEffectInfo("BOW_108_04_SKILL_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SKILL_DAMAGE,
                       0.1, 10, 99),
        BuffEffectInfo("BOW_108_04_SPB_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SP_RATE, 0.1, 10, 0)
    }
    on_0_plus_buffs = {
        BuffEffectInfo("BOW_108_04_DEF_LV03", HitTargetSimple.SELF, BuffParameter.DEF_BUFF, 0.1, 10, 0)
    }
    on_1_plus_buffs = on_0_plus_buffs | {
        BuffEffectInfo("BOW_108_04_CRTDMG_LV03", HitTargetSimple.SELF, BuffParameter.CRT_DAMAGE, 0.1, 10, 0)
    }
    on_2_plus_buffs = on_1_plus_buffs | {
        BuffEffectInfo("BOW_108_04_SP_LV03", HitTargetSimple.SELF, BuffParameter.SP_CHARGE_PCT_S1, 1, 0, 0)
    }

    expected_buffs_lv_max = {
        ConditionComposite(Condition.COVER_TEAMMATE_0): base_buffs_at_max | on_0_plus_buffs,
        ConditionComposite(Condition.COVER_TEAMMATE_1): base_buffs_at_max | on_1_plus_buffs,
        ConditionComposite(Condition.COVER_TEAMMATE_2): base_buffs_at_max | on_2_plus_buffs,
        ConditionComposite(Condition.COVER_TEAMMATE_3): base_buffs_at_max | on_2_plus_buffs,
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        check_buff_unit_match(
            entry.max_lv_buffs, expected_buffs_lv_max[entry.condition_comp], message=entry.condition_comp
        )
        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"


def test_has_pre_condition(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica
    skill_data = transformer_skill.transform_supportive(107505011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buffs_lv_max = {
        ConditionComposite(Condition.SELF_HP_GTE_50): {
            BuffEffectInfo("BUF_200_DMG_LV04", HitTargetSimple.SELF, BuffParameter.HP_DECREASE_BY_MAX, 0.1, 0, 0),
            BuffEffectInfo("BUF_200_SPC_LV04", HitTargetSimple.SELF, BuffParameter.SP_CHARGE_PCT_USED, 0.2, 0, 0)
        }
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        check_buff_unit_match(
            entry.max_lv_buffs, expected_buffs_lv_max[entry.condition_comp], message=entry.condition_comp
        )
        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"
