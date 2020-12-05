from dlparse.enums import BuffParameter, HitTargetSimple, SkillCondition, SkillConditionComposite
from dlparse.model import SupportiveSkillUnit
from dlparse.transformer import SkillTransformer


def test_no_condition(transformer_skill: SkillTransformer):
    # Kirsty S2
    # https://dragalialost.gamepedia.com/Kirsty
    skill_data = transformer_skill.transform_supportive(105503022)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buffs_lv_max = {
        SkillConditionComposite(): {
            SupportiveSkillUnit(
                target=HitTargetSimple.TEAM,
                parameter=BuffParameter.ATK,
                rate=0.25,
                duration_time=15,
                duration_count=0,
                hit_attr_label="BUF_ALL_ATK_SSR_30_LV03",
                action_cond_id=302030501,
                max_stack_count=0
            ),
        },
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.max_lv_buffs == expected_buffs_lv_max[entry.condition_comp], entry.condition_comp
        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"


def test_element_restricted(transformer_skill: SkillTransformer):
    # Emma S1
    # https://dragalialost.gamepedia.com/Emma
    skill_data = transformer_skill.transform_supportive(105401031)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buffs_lv_max = {
        SkillConditionComposite(SkillCondition.TARGET_ELEM_FLAME): {
            SupportiveSkillUnit(
                target=HitTargetSimple.TEAM,
                parameter=BuffParameter.ATK,
                rate=0.25,
                duration_time=15,
                duration_count=0,
                hit_attr_label="BUF_160_ATK_FIRE_LV03",
                action_cond_id=167,
                max_stack_count=0
            ),
        },
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.max_lv_buffs == expected_buffs_lv_max[entry.condition_comp], entry.condition_comp
        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"


def test_teammate_coverage(transformer_skill: SkillTransformer):
    # Summer Cleo S2
    # https://dragalialost.gamepedia.com/Summer_Cleo
    skill_data = transformer_skill.transform_supportive(106504012)

    possible_entries = skill_data.get_all_possible_entries()

    base_buffs_at_max = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.05,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_ATK_LV03",
            action_cond_id=76,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.CRT_RATE,
            rate=0.03,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRT_LV03",
            action_cond_id=38,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=99,
            hit_attr_label="BOW_108_04_SKILL_LV03",
            action_cond_id=197,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SP_RATE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_SPB_LV03",
            action_cond_id=194,
            max_stack_count=0
        ),
    }
    on_0_plus_buffs = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.DEF,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_DEF_LV03",
            action_cond_id=303020101,
            max_stack_count=0
        )
    }
    on_1_plus_buffs = on_0_plus_buffs | {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.CRT_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRTDMG_LV03",
            action_cond_id=1176,
            max_stack_count=0
        )
    }
    on_2_plus_buffs = on_1_plus_buffs | {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.SP_CHARGE_PCT_S1,
            rate=1,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BOW_108_04_SP_LV03",
            action_cond_id=0,
            max_stack_count=0
        )
    }

    expected_buffs_lv_max = {
        SkillConditionComposite(SkillCondition.COVER_TEAMMATE_0): base_buffs_at_max | on_0_plus_buffs,
        SkillConditionComposite(SkillCondition.COVER_TEAMMATE_1): base_buffs_at_max | on_1_plus_buffs,
        SkillConditionComposite(SkillCondition.COVER_TEAMMATE_2): base_buffs_at_max | on_2_plus_buffs,
        SkillConditionComposite(SkillCondition.COVER_TEAMMATE_3): base_buffs_at_max | on_2_plus_buffs,
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.max_lv_buffs == expected_buffs_lv_max[entry.condition_comp], entry.condition_comp
        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"


def test_has_pre_condition(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica
    skill_data = transformer_skill.transform_supportive(107505011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buffs_lv_max = {
        SkillConditionComposite(SkillCondition.SELF_HP_GTE_50): {
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.HP_DECREASE_BY_MAX,
                rate=0.1,
                duration_time=0,
                duration_count=0,
                hit_attr_label="BUF_200_DMG_LV04",
                action_cond_id=0,
                max_stack_count=0
            ),
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.SP_CHARGE_PCT_USED,
                rate=0.2,
                duration_time=0,
                duration_count=0,
                hit_attr_label="BUF_200_SPC_LV04",
                action_cond_id=0,
                max_stack_count=0
            )
        }
    }

    assert set(expected_buffs_lv_max.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.max_lv_buffs == expected_buffs_lv_max[entry.condition_comp], entry.condition_comp
        del expected_buffs_lv_max[entry.condition_comp]

    assert len(expected_buffs_lv_max) == 0, f"Conditions not tested: {set(expected_buffs_lv_max.keys())}"
