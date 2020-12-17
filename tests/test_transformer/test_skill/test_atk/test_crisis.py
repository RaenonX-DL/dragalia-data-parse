from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_bellina_s2(transformer_skill: SkillTransformer):
    # Bellina S2
    # https://dragalialost.gamepedia.com/Bellina
    skill_data = transformer_skill.transform_attacking(103505034).with_conditions()

    assert skill_data.crisis_mods == approx_matrix([
        [3],
        [3]
    ])


def test_veronica_s1(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica
    skill_data = transformer_skill.transform_attacking(107505011).with_conditions()

    assert skill_data.crisis_mods == approx_matrix([
        [2.25] * 4,
        [2.25] * 4,
        [2.25] * 4,
        [1.5] * 4
    ])
