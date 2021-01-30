from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_wedding_elisanne_s1(transformer_skill: SkillTransformer):
    # Wedding Elisanne S1
    # https://dragalialost.wiki/w/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503021).with_conditions()

    assert not any(skill_data.dispel_buff)
    assert not skill_data.dispel_buff_at_max
    assert skill_data.dispel_timings == [[], [], []]


def test_og_ranzal_s1(transformer_skill: SkillTransformer):
    # Original Ranzal S1
    # https://dragalialost.wiki/w/Ranzal
    skill_data = transformer_skill.transform_attacking(104403011).with_conditions()

    assert skill_data.dispel_buff == [False, False, False, True]
    assert skill_data.dispel_buff_at_max
    assert skill_data.dispel_timings == [[], [], [], [0.0]]


def test_nadine_s1(transformer_skill: SkillTransformer):
    # Nadine S1
    # https://dragalialost.wiki/w/Nadine
    skill_data = transformer_skill.transform_attacking(105501021).with_conditions()

    assert all(skill_data.dispel_buff)
    assert skill_data.dispel_buff_at_max
    assert skill_data.dispel_timings == approx_matrix([[0.466666669], [0.466666669], [0.466666669]])


def test_gala_alex_s1_chained_buffed(transformer_skill: SkillTransformer):
    # Gala Alex S1 (Target Buffed)
    # https://dragalialost.wiki/w/Gala_Alex
    skill_data = transformer_skill.transform_attacking(101505024).with_conditions()

    assert all(skill_data.dispel_buff)
    assert skill_data.dispel_buff_at_max
    assert skill_data.dispel_timings == approx_matrix([
        [0.166666672, 0.366666675, 0.6],
        [0.166666672, 0.366666675, 0.6],
        [0.166666672, 0.366666675, 0.6]
    ])
