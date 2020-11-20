import pytest

from dlparse.errors import SkillDataNotFound
from dlparse.transformer import SkillTransformer


def test_skill_not_found(transformer_skill: SkillTransformer):
    with pytest.raises(SkillDataNotFound) as error:
        transformer_skill.transform_attacking(87)

        assert error.value.skill_id == 87


def test_single_hit_1(transformer_skill: SkillTransformer):
    # Wedding Elisanne S1
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503021)

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == [12.03, 13.38, 14.85]
    assert skill_data.total_mod_at_max == 14.85
    assert skill_data.mods == [[12.03], [13.38], [14.85]]
    assert skill_data.mods_at_max == [14.85]
    assert skill_data.max_available_level == 3


def test_single_hit_2(transformer_skill: SkillTransformer):
    # Wedding Elisanne S2
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503022)

    assert skill_data.hit_count == [1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == [10.02, 10.515]
    assert skill_data.total_mod_at_max == 10.515
    assert skill_data.mods == [[10.02], [10.515]]
    assert skill_data.mods_at_max == [10.515]
    assert skill_data.max_available_level == 2


def test_single_projectile(transformer_skill: SkillTransformer):
    # Euden S2
    # https://dragalialost.gamepedia.com/The_Prince
    skill_data = transformer_skill.transform_attacking(101401012)

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == [11.94, 13.27, 14.74]
    assert skill_data.total_mod_at_max == 14.74
    assert skill_data.mods == [[11.94], [13.27], [14.74]]
    assert skill_data.mods_at_max == [14.74]
    assert skill_data.max_available_level == 3


def test_multi_hits_same_damage_1(transformer_skill: SkillTransformer):
    # Templar Hope S2
    # https://dragalialost.gamepedia.com/Templar_Hope
    # Mods for 70 MC has already inserted, but not yet released
    skill_data = transformer_skill.transform_attacking(101403022)

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == [22.7, 26.48, 28.0]
    assert skill_data.total_mod_at_max == 28.0
    assert skill_data.mods == [[11.35, 11.35], [13.24, 13.24], [14.0, 14.0]]
    assert skill_data.mods_at_max == [14.0, 14.0]
    assert skill_data.max_available_level == 3


def test_multi_hits_same_damage_2(transformer_skill: SkillTransformer):
    # Ranzal S1
    # https://dragalialost.gamepedia.com/Ranzal
    skill_data = transformer_skill.transform_attacking(104403011)

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == [18.72, 20.8, 23.12, 28.912]
    assert skill_data.total_mod_at_max == 28.912
    assert skill_data.mods == [[4.68] * 4, [5.2] * 4, [5.78] * 4, [7.228] * 4]
    assert skill_data.mods_at_max == [7.228] * 4
    assert skill_data.max_available_level == 4


def test_multi_hits_different_damage_1(transformer_skill: SkillTransformer):
    # Summer Julietta S1
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data = transformer_skill.transform_attacking(104502011)

    assert skill_data.hit_count == [3, 3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([22.352, 23.452, 24.64, 27.082])
    assert skill_data.total_mod_at_max == 27.082
    assert skill_data.mods == [
        [11.176, 3.344, 7.832], [11.726, 3.52, 8.206], [12.32, 3.696, 8.624], [13.552, 4.048, 9.482]
    ]
    assert skill_data.mods_at_max == [13.552, 4.048, 9.482]
    assert skill_data.max_available_level == 4


def test_multi_hits_different_damage_2(transformer_skill: SkillTransformer):
    # Gala Euden S2
    # https://dragalialost.gamepedia.com/Gala_Prince
    skill_data = transformer_skill.transform_attacking(101504032)

    assert skill_data.hit_count == [13] * 2
    assert skill_data.hit_count_at_max == 13
    assert skill_data.total_mod == pytest.approx([1.2 * 3 + 3.6 * 10, 1.34 * 3 + 4 * 10])
    assert skill_data.total_mod_at_max == pytest.approx(44.02)
    assert skill_data.mods == [
        [1.2] + [3.6] + [1.2] * 2 + [3.6] * 9,
        [1.34] + [4] + [1.34] * 2 + [4] * 9,
    ]
    assert skill_data.mods_at_max == [1.34] + [4] + [1.34] * 2 + [4] * 9
    assert skill_data.max_available_level == 2


def test_has_dummy_hits(transformer_skill: SkillTransformer):
    # Renee S1
    # https://dragalialost.gamepedia.com/Renee
    skill_data = transformer_skill.transform_attacking(103402031)

    assert skill_data.hit_count == [6, 6, 6, 6]
    assert skill_data.hit_count_at_max == 6
    assert skill_data.total_mod == pytest.approx([16.98, 17.82, 18.66, 18.78])
    assert skill_data.total_mod_at_max == pytest.approx(18.78)
    assert skill_data.mods == [[2.83] * 6, [2.97] * 6, [3.11] * 6, [3.13] * 6]
    assert skill_data.mods_at_max == [3.13] * 6
    assert skill_data.max_available_level == 4


def test_buff_related(transformer_skill: SkillTransformer):
    # Karina S1
    # https://dragalialost.gamepedia.com/Karina
    skill_data = transformer_skill.transform_attacking(104402011)

    assert skill_data.hit_count == [2, 2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([5.96 * 2, 6.63 * 2, 7.36 * 2, 8.18 * 2])
    assert skill_data.total_mod_at_max == pytest.approx(16.36)
    assert skill_data.mods == [[5.96] * 2, [6.63] * 2, [7.36] * 2, [8.18] * 2]
    assert skill_data.mods_at_max == [8.18] * 2
    assert skill_data.max_available_level == 4


def test_sigil_released(transformer_skill: SkillTransformer):
    # Nevin S2
    # https://dragalialost.gamepedia.com/Nevin
    pass
