from dlparse.enums import Condition, ConditionComposite, Status
from dlparse.transformer import SkillTransformer
from tests.utils import AfflictionInfo, check_affliction_unit_match


def test_og_alex_s1_poison(transformer_skill: SkillTransformer):
    # Original Alex S1
    # https://dragalialost.wiki/w/Alex
    skill_data = transformer_skill.transform_attacking(103405021).with_conditions()

    afflictions_lv1 = []
    afflictions_lv2 = ([AfflictionInfo("DAG_117_03_H01_POISON_LV02", Status.POISON, 90, 15, 2.9, 0.28, True)] * 3
                       + [AfflictionInfo("DAG_117_03_H02_POISON_LV02", Status.POISON, 90, 15, 2.9, 0.28, True)] * 1)
    afflictions_lv3 = ([AfflictionInfo("DAG_117_03_H01_POISON_LV03", Status.POISON, 100, 15, 2.9, 0.396, True)] * 3
                       + [AfflictionInfo("DAG_117_03_H02_POISON_LV03", Status.POISON, 100, 15, 2.9, 0.396, True)] * 1)

    expected_afflictions = [afflictions_lv1, afflictions_lv2, afflictions_lv3]

    assert len(expected_afflictions) == len(skill_data.afflictions)

    for skill_lv, (expected, actual) in enumerate(zip(expected_afflictions, skill_data.afflictions), start=1):
        check_affliction_unit_match(actual, expected, message=skill_lv)


def test_peony_s1_paralyze(transformer_skill: SkillTransformer):
    # Peony S1
    # https://dragalialost.wiki/w/Peony
    skill_data = transformer_skill.transform_attacking(107504021).with_conditions()

    afflictions_lv1 = [AfflictionInfo("ROD_112_04_H01_LV01", Status.PARALYZE, 100, 13, 3.9, 0.513, True)]
    afflictions_lv2 = [AfflictionInfo("ROD_112_04_H01_LV02", Status.PARALYZE, 110, 13, 3.9, 0.727, True)]
    afflictions_lv3 = [AfflictionInfo("ROD_112_04_H01_LV03", Status.PARALYZE, 120, 13, 3.9, 0.97, True)]

    expected_afflictions = [afflictions_lv1, afflictions_lv2, afflictions_lv3]

    assert len(expected_afflictions) == len(skill_data.afflictions)

    for skill_lv, (expected, actual) in enumerate(zip(expected_afflictions, skill_data.afflictions), start=1):
        check_affliction_unit_match(actual, expected, message=skill_lv)


def test_meene_s2_6_butterflies_poison(transformer_skill: SkillTransformer):
    # Meene S2
    # https://dragalialost.wiki/w/Meene
    skill_data_base = transformer_skill.transform_attacking(106503036)

    expected_addl_at_max = {
        ConditionComposite([Condition.BULLETS_SUMMONED_0]): 0,
        ConditionComposite([Condition.BULLETS_SUMMONED_1]): 1,
        ConditionComposite([Condition.BULLETS_SUMMONED_2]): 2,
        ConditionComposite([Condition.BULLETS_SUMMONED_3]): 3,
        ConditionComposite([Condition.BULLETS_SUMMONED_4]): 4,
        ConditionComposite([Condition.BULLETS_SUMMONED_5]): 5,
        ConditionComposite([Condition.BULLETS_SUMMONED_6]): 6,
        ConditionComposite([Condition.BULLETS_SUMMONED_7]): 7,
        ConditionComposite([Condition.BULLETS_SUMMONED_8]): 8,
        ConditionComposite([Condition.BULLETS_SUMMONED_9]): 9,
    }

    for condition_comp, addl_hit in expected_addl_at_max.items():
        skill_data = skill_data_base.with_conditions(condition_comp)

        afflictions_lv1 = (
                [AfflictionInfo("BOW_118_04_PLUS_H01_LV01", Status.POISON, 110, 15, 2.9, 0.436, True)] * 1
                + [AfflictionInfo("BOW_118_04_PLUS_H02_LV01", Status.POISON, 110, 15, 2.9, 0.436, True)] * addl_hit
        )
        afflictions_lv2 = (
                [AfflictionInfo("BOW_118_04_PLUS_H01_LV02", Status.POISON, 120, 15, 2.9, 0.582, True)] * 1
                + [AfflictionInfo("BOW_118_04_PLUS_H02_LV02", Status.POISON, 120, 15, 2.9, 0.582, True)] * addl_hit
        )

        expected_afflictions = [afflictions_lv1, afflictions_lv2]

        assert len(expected_afflictions) == len(skill_data.afflictions)

        for skill_lv, (expected, actual) in enumerate(zip(expected_afflictions, skill_data.afflictions), start=1):
            check_affliction_unit_match(actual, expected, message=[skill_lv, condition_comp])
