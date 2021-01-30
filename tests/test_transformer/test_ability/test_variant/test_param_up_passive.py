from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_resist_1(transformer_ability: AbilityTransformer):
    # Marty (AB3 @ Max - Stun Res +50%)
    # https://dragalialost.wiki/w/Marty
    ability_data = transformer_ability.transform_ability(110020604)

    expected_info = {
        AbilityEffectInfo(110020604, ConditionComposite(), BuffParameter.RESISTANCE_STUN, 0.5),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_resist_2(transformer_ability: AbilityTransformer):
    # Wedding Elisanne (AB2 @ Max - Bog Res +100%)
    # https://dragalialost.wiki/w/Wedding_Elisanne
    ability_data = transformer_ability.transform_ability(110020906)

    expected_info = {
        AbilityEffectInfo(110020906, ConditionComposite(), BuffParameter.RESISTANCE_BOG, 1.0),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_potent_resist_1(transformer_ability: AbilityTransformer):
    # Marty (AB2 @ Max - Stun Res +50% & ATK +15% 10s, CD 15s)
    # https://dragalialost.wiki/w/Marty
    ability_data = transformer_ability.transform_ability(676)

    expected_info = {
        AbilityEffectInfo(
            676, ConditionComposite(), BuffParameter.RESISTANCE_STUN, 0.5, cooldown_sec=0
        ),
        AbilityEffectInfo(
            677, ConditionComposite(Condition.ON_HIT_BY_STUN), BuffParameter.ATK_BUFF, 0.15, cooldown_sec=15
        ),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_potent_resist_2(transformer_ability: AbilityTransformer):
    # Summer Julietta (AB2 @ Max - Stun Res +100% & ATK +15% 10s, CD 15s)
    # https://dragalialost.wiki/w/Marty
    ability_data = transformer_ability.transform_ability(678)

    expected_info = {
        AbilityEffectInfo(
            678, ConditionComposite(), BuffParameter.RESISTANCE_STUN, 1.0, cooldown_sec=0
        ),
        AbilityEffectInfo(
            701, ConditionComposite(Condition.ON_HIT_BY_STUN), BuffParameter.ATK_BUFF, 0.15, cooldown_sec=15
        ),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_potent_resist_3(transformer_ability: AbilityTransformer):
    # Summer Cleo S2 (AB2 @ Max - Curse Res +100% & ATK +15% 10s, CD 15s)
    # https://dragalialost.wiki/w/Summer_Cleo
    ability_data = transformer_ability.transform_ability(937)

    expected_info = {
        AbilityEffectInfo(
            937, ConditionComposite(), BuffParameter.RESISTANCE_CURSE, 1.0, cooldown_sec=0
        ),
        AbilityEffectInfo(
            685, ConditionComposite(Condition.ON_HIT_BY_CURSE), BuffParameter.ATK_BUFF, 0.15, cooldown_sec=15
        ),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_sp_rate_up(transformer_ability: AbilityTransformer):
    # Marty (AB1 @ Max - SP Rate +10%)
    # https://dragalialost.wiki/w/Marty
    ability_data = transformer_ability.transform_ability(938)

    expected_info = {
        AbilityEffectInfo(938, ConditionComposite(), BuffParameter.SP_RATE, 0.1),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_atk_up_full_hp(transformer_ability: AbilityTransformer):
    # Yukata Cassandra (AB1 @ Max - ATK +20% when HP = 100%)
    # https://dragalialost.wiki/w/Yukata_Cassandra
    ability_data = transformer_ability.transform_ability(210000307)

    expected_info = {
        AbilityEffectInfo(210000307, ConditionComposite(Condition.SELF_HP_FULL), BuffParameter.ATK_PASSIVE, 0.2),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_atk_up_gte_70_hp(transformer_ability: AbilityTransformer):
    # Karl (AB1 @ Max - RP +13% when HP = 100%)
    # https://dragalialost.wiki/w/Karl
    ability_data = transformer_ability.transform_ability(719)

    expected_info = {
        AbilityEffectInfo(719, ConditionComposite(Condition.SELF_HP_GTE_70), BuffParameter.ATK_PASSIVE, 0.15),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)
