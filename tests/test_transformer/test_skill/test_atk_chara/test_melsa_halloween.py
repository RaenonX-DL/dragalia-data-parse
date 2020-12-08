from dlparse.transformer import SkillTransformer


def test_s2(transformer_skill: SkillTransformer):
    # Halloween Melsa S2
    # https://dragalialost.gamepedia.com/Halloween_Melsa
    skill_data = transformer_skill.transform_attacking(105503032).with_conditions()

    assert skill_data.hit_count == [3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == [1.1 * 3, 1.4 * 3]
    assert skill_data.total_mod_at_max == 1.4 * 3
    assert skill_data.mods == [[1.1] * 3, [1.4] * 3]
    assert skill_data.mods_at_max == [1.4] * 3
    assert skill_data.max_level == 2
