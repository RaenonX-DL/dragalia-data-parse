from dlparse.enums import Status
from dlparse.model import SkillAfflictionUnit
from dlparse.transformer import SkillTransformer


def test_og_alex_s1_poison(transformer_skill: SkillTransformer):
    # Alex S1
    # https://dragalialost.gamepedia.com/Alex
    skill_data = transformer_skill.transform_attacking(103405021)

    afflictions_lv1 = []
    afflictions_lv2 = [
        SkillAfflictionUnit(
            status=Status.POISON,
            time=0.3,
            rate_percent=90,
            duration=12,
            interval=2.9,
            damage_mod=0.28,
            stackable=True,
            hit_attr_label="DAG_117_03_H01_POISON_LV02",
            action_cond_id=101020501
        ),
        SkillAfflictionUnit(
            status=Status.POISON,
            time=0.73333349,
            rate_percent=90,
            duration=12,
            interval=2.9,
            damage_mod=0.28,
            stackable=True,
            hit_attr_label="DAG_117_03_H01_POISON_LV02",
            action_cond_id=101020501
        ),
        SkillAfflictionUnit(
            status=Status.POISON,
            time=0.9,
            rate_percent=90,
            duration=12,
            interval=2.9,
            damage_mod=0.28,
            stackable=True,
            hit_attr_label="DAG_117_03_H01_POISON_LV02",
            action_cond_id=101020501
        ),
        SkillAfflictionUnit(
            status=Status.POISON,
            time=1.466666667,
            rate_percent=90,
            duration=12,
            interval=2.9,
            damage_mod=0.28,
            stackable=True,
            hit_attr_label="DAG_117_03_H02_POISON_LV02",
            action_cond_id=101020501
        ),
    ]
    afflictions_lv3 = [
        SkillAfflictionUnit(
            status=Status.POISON,
            time=0.3,
            rate_percent=100,
            duration=12,
            interval=2.9,
            damage_mod=0.396,
            stackable=True,
            hit_attr_label="DAG_117_03_H01_POISON_LV03",
            action_cond_id=101020601
        ),
        SkillAfflictionUnit(
            status=Status.POISON,
            time=0.73333349,
            rate_percent=100,
            duration=12,
            interval=2.9,
            damage_mod=0.396,
            stackable=True,
            hit_attr_label="DAG_117_03_H01_POISON_LV03",
            action_cond_id=101020601
        ),
        SkillAfflictionUnit(
            status=Status.POISON,
            time=0.9,
            rate_percent=100,
            duration=12,
            interval=2.9,
            damage_mod=0.396,
            stackable=True,
            hit_attr_label="DAG_117_03_H01_POISON_LV03",
            action_cond_id=101020601
        ),
        SkillAfflictionUnit(
            status=Status.POISON,
            time=1.466666667,
            rate_percent=100,
            duration=12,
            interval=2.9,
            damage_mod=0.396,
            stackable=True,
            hit_attr_label="DAG_117_03_H02_POISON_LV03",
            action_cond_id=101020601
        ),
    ]

    expected_afflictions = [afflictions_lv1, afflictions_lv2, afflictions_lv3]

    assert len(expected_afflictions) == len(skill_data.afflictions)

    for skill_lv, (expected, actual) in enumerate(zip(expected_afflictions, skill_data.afflictions), start=1):
        assert expected == actual, skill_lv


def test_peony_s1_paralyze(transformer_skill: SkillTransformer):
    # Peony S1
    # https://dragalialost.gamepedia.com/Peony
    skill_data = transformer_skill.transform_attacking(107504021)

    afflictions_lv1 = [
        SkillAfflictionUnit(
            status=Status.PARALYZE,
            time=0.6666667,
            rate_percent=100,
            duration=13,
            interval=3.9,
            damage_mod=0.513,
            stackable=True,
            hit_attr_label="ROD_112_04_H01_LV01",
            action_cond_id=104031001
        ),
    ]
    afflictions_lv2 = [
        SkillAfflictionUnit(
            status=Status.PARALYZE,
            time=0.6666667,
            rate_percent=110,
            duration=13,
            interval=3.9,
            damage_mod=0.727,
            stackable=True,
            hit_attr_label="ROD_112_04_H01_LV02",
            action_cond_id=104031101
        ),
    ]
    afflictions_lv3 = [
        SkillAfflictionUnit(
            status=Status.PARALYZE,
            time=0.6666667,
            rate_percent=120,
            duration=13,
            interval=3.9,
            damage_mod=0.97,
            stackable=True,
            hit_attr_label="ROD_112_04_H01_LV03",
            action_cond_id=104031201
        ),
    ]

    expected_afflictions = [afflictions_lv1, afflictions_lv2, afflictions_lv3]

    assert len(expected_afflictions) == len(skill_data.afflictions)

    for skill_lv, (expected, actual) in enumerate(zip(expected_afflictions, skill_data.afflictions), start=1):
        assert expected == actual, skill_lv

# TODO: More complicating affliction processes and tests
