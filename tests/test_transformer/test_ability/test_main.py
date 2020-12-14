from dlparse.transformer import AbilityTransformer


def test_all_skill_prep(transformer_ability: AbilityTransformer):
    # Veronica (AB3 @ Max - Skill prep & skill fill 5%)
    # https://dragalialost.gamepedia.com/Veronica

    ability_data = transformer_ability.transform_ability(721)

    # FIXME: Add some tests to imply the possible usages
    #   - Keep condition values, only transform "onSkill" to be also the condition
    #   - Transform effects
    # FIXME: [PRIO] Steps for dev
    #   - try transform all
    #   - find the best internal data structure for exporting
