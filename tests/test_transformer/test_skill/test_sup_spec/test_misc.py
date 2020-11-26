from dlparse.transformer import SkillTransformer


def test_partial_attacking(transformer_skill: SkillTransformer):
    # Elisanne S1
    # https://dragalialost.gamepedia.com/Elisanne
    skill_data = transformer_skill.transform_supportive(105402011)

    # TEST: TBA - OG!Elisanne S1
