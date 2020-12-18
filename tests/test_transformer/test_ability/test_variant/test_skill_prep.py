from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test(transformer_ability: AbilityTransformer):
    # Veronica (AB3 @ Max - Skill prep & skill fill 5%)
    # https://dragalialost.gamepedia.com/Veronica

    ability_data = transformer_ability.transform_ability(721)

    cond_quest_start = ConditionComposite(Condition.QUEST_START)
    cond_skill_used = ConditionComposite(Condition.SKILL_USED_ALL)

    expected_info = {
        AbilityEffectInfo(721, cond_quest_start, BuffParameter.SP_CHARGE_PCT_S1, 1),
        AbilityEffectInfo(721, cond_quest_start, BuffParameter.SP_CHARGE_PCT_S2, 1),
        AbilityEffectInfo(721, cond_quest_start, BuffParameter.SP_CHARGE_PCT_S3, 1),
        AbilityEffectInfo(721, cond_quest_start, BuffParameter.SP_CHARGE_PCT_S4, 1),
        AbilityEffectInfo(723, cond_skill_used, BuffParameter.SP_CHARGE_PCT_S1, 0.05),
        AbilityEffectInfo(723, cond_skill_used, BuffParameter.SP_CHARGE_PCT_S2, 0.05),
        AbilityEffectInfo(723, cond_skill_used, BuffParameter.SP_CHARGE_PCT_S3, 0.05),
        AbilityEffectInfo(723, cond_skill_used, BuffParameter.SP_CHARGE_PCT_S4, 0.05),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)
