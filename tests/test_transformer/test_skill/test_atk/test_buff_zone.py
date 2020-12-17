from dlparse.model import BuffZoneBoostData
from dlparse.transformer import SkillTransformer


def test_self_ally_diff(transformer_skill: SkillTransformer):
    # Nevin S2 @ Sigil Released
    # https://dragalialost.gamepedia.com/Nevin
    skill_data = transformer_skill.transform_attacking(103505044, is_exporting=True).with_conditions()

    assert skill_data.buff_zone_boost_mtx == [BuffZoneBoostData(2.7, 0.9), BuffZoneBoostData(3, 1)]


def test_self_ally_same(transformer_skill: SkillTransformer):
    # Dragonyule Victor S2
    # https://dragalialost.gamepedia.com/Dragonyule_Victor
    skill_data = transformer_skill.transform_attacking(104505032, is_exporting=True).with_conditions()

    assert skill_data.buff_zone_boost_mtx == [BuffZoneBoostData(4.5, 4.5), BuffZoneBoostData(5, 5)]
