from dlparse.enums import Status
from dlparse.transformer import SkillTransformer
from tests.utils import AfflictionInfo, check_affliction_unit_match


def test_og_alex_s1_poison(transformer_skill: SkillTransformer):
    # Original Alex S1
    # https://dragalialost.gamepedia.com/Alex
    skill_data = transformer_skill.transform_attacking(103405021)

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
    # https://dragalialost.gamepedia.com/Peony
    skill_data = transformer_skill.transform_attacking(107504021)

    afflictions_lv1 = [AfflictionInfo("ROD_112_04_H01_LV01", Status.PARALYZE, 100, 13, 3.9, 0.513, True)]
    afflictions_lv2 = [AfflictionInfo("ROD_112_04_H01_LV02", Status.PARALYZE, 110, 13, 3.9, 0.727, True)]
    afflictions_lv3 = [AfflictionInfo("ROD_112_04_H01_LV03", Status.PARALYZE, 120, 13, 3.9, 0.97, True)]

    expected_afflictions = [afflictions_lv1, afflictions_lv2, afflictions_lv3]

    assert len(expected_afflictions) == len(skill_data.afflictions)

    for skill_lv, (expected, actual) in enumerate(zip(expected_afflictions, skill_data.afflictions), start=1):
        check_affliction_unit_match(actual, expected, message=skill_lv)

# TODO: More complicating affliction processes and tests
