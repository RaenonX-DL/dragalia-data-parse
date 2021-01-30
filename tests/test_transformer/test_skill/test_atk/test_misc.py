from dlparse.transformer import SkillTransformer


def test_max_level_specified(transformer_skill: SkillTransformer):
    # Templar Hope S2
    # https://dragalialost.wiki/w/Templar_Hope
    skill_data = transformer_skill.transform_attacking(101403022, max_lv=2).with_conditions()

    assert skill_data.hit_count == [2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == [22.7, 26.48]
    assert skill_data.total_mod_at_max == 26.48
    assert skill_data.mods == [[11.35, 11.35], [13.24, 13.24]]
    assert skill_data.mods_at_max == [13.24, 13.24]
    assert skill_data.max_level == 2
