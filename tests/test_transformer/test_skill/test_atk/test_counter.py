from dlparse.transformer import SkillTransformer


def test_cassandra_s2(transformer_skill: SkillTransformer):
    # Cassandra S2
    # https://dragalialost.wiki/w/Cassandra
    skill_data = transformer_skill.transform_attacking(107505032).with_conditions()

    assert skill_data.counter_mods == [[11.0, 0, 0, 0, 0], [11.0, 0, 0, 0, 0], [11.0, 0, 0, 0, 0]]
    assert skill_data.counter_mod_at_max == [11.0, 0, 0, 0, 0]
    assert skill_data.total_counter_mod == [11, 11, 11]
    assert skill_data.total_counter_mod_at_max == 11


def test_lea_s2(transformer_skill: SkillTransformer):
    # Lea S2
    # https://dragalialost.wiki/w/Lea
    skill_data = transformer_skill.transform_attacking(101501032).with_conditions()

    assert skill_data.counter_mods == [[11.0, 0], [11.0, 0], [11.0, 0]]
    assert skill_data.counter_mod_at_max == [11.0, 0]
    assert skill_data.total_counter_mod == [11, 11, 11]
    assert skill_data.total_counter_mod_at_max == 11


def test_delphi_s2(transformer_skill: SkillTransformer):
    # Delphi S2
    # https://dragalialost.wiki/w/Delphi
    skill_data = transformer_skill.transform_attacking(103505022).with_conditions()

    assert skill_data.counter_mods == [[11.0, 0], [11.0, 0], [11.0, 0]]
    assert skill_data.counter_mod_at_max == [11.0, 0]
    assert skill_data.total_counter_mod == [11, 11, 11]
    assert skill_data.total_counter_mod_at_max == 11
