import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.errors import SkillDataNotFoundError
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_skill_not_found(transformer_skill: SkillTransformer):
    with pytest.raises(SkillDataNotFoundError) as error:
        transformer_skill.transform_attacking(87)

        assert error.value.skill_id == 87


def test_single_hit_1(transformer_skill: SkillTransformer):
    # Wedding Elisanne S1
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503021).with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == [12.03, 13.38, 14.85]
    assert skill_data.total_mod_at_max == 14.85
    assert skill_data.mods == [[12.03], [13.38], [14.85]]
    assert skill_data.mods_at_max == [14.85]
    assert skill_data.max_level == 3


def test_single_hit_2(transformer_skill: SkillTransformer):
    # Wedding Elisanne S2
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503022).with_conditions()

    assert skill_data.hit_count == [1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == [10.02, 10.515]
    assert skill_data.total_mod_at_max == 10.515
    assert skill_data.mods == [[10.02], [10.515]]
    assert skill_data.mods_at_max == [10.515]
    assert skill_data.max_level == 2


def test_single_projectile(transformer_skill: SkillTransformer):
    # Euden S2
    # https://dragalialost.gamepedia.com/The_Prince
    skill_data = transformer_skill.transform_attacking(101401012).with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == [11.94, 13.27, 14.74]
    assert skill_data.total_mod_at_max == 14.74
    assert skill_data.mods == [[11.94], [13.27], [14.74]]
    assert skill_data.mods_at_max == [14.74]
    assert skill_data.max_level == 3


def test_multi_hits_same_damage_1(transformer_skill: SkillTransformer):
    # Templar Hope S2
    # https://dragalialost.gamepedia.com/Templar_Hope
    # Mods for 70 MC has already inserted, but not yet released
    skill_data = transformer_skill.transform_attacking(101403022).with_conditions()

    assert skill_data.hit_count == [2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == [22.7, 26.48, 28.0]
    assert skill_data.total_mod_at_max == 28.0
    assert skill_data.mods == [[11.35, 11.35], [13.24, 13.24], [14.0, 14.0]]
    assert skill_data.mods_at_max == [14.0, 14.0]
    assert skill_data.max_level == 3


def test_multi_hits_same_damage_2(transformer_skill: SkillTransformer):
    # Ranzal S1
    # https://dragalialost.gamepedia.com/Ranzal
    skill_data = transformer_skill.transform_attacking(104403011).with_conditions()

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == [18.72, 20.8, 23.12, 28.912]
    assert skill_data.total_mod_at_max == 28.912
    assert skill_data.mods == [[4.68] * 4, [5.2] * 4, [5.78] * 4, [7.228] * 4]
    assert skill_data.mods_at_max == [7.228] * 4
    assert skill_data.max_level == 4


def test_multi_hits_different_damage_1(transformer_skill: SkillTransformer):
    # Summer Julietta S1
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data = transformer_skill.transform_attacking(104502011).with_conditions()

    assert skill_data.hit_count == [3, 3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([22.352, 23.452, 24.64, 27.082])
    assert skill_data.total_mod_at_max == 27.082
    assert skill_data.mods == [
        [11.176, 3.344, 7.832], [11.726, 3.52, 8.206], [12.32, 3.696, 8.624], [13.552, 4.048, 9.482]
    ]
    assert skill_data.mods_at_max == [13.552, 4.048, 9.482]
    assert skill_data.max_level == 4


def test_multi_hits_different_damage_2(transformer_skill: SkillTransformer):
    # Gala Euden S2
    # https://dragalialost.gamepedia.com/Gala_Prince
    skill_data = transformer_skill.transform_attacking(101504032).with_conditions()

    assert skill_data.hit_count == [13] * 2
    assert skill_data.hit_count_at_max == 13
    assert skill_data.total_mod == pytest.approx([1.2 * 3 + 3.6 * 10, 1.34 * 3 + 4 * 10])
    assert skill_data.total_mod_at_max == pytest.approx(44.02)
    assert skill_data.mods == [
        [1.2] + [3.6] + [1.2] * 2 + [3.6] * 9,
        [1.34] + [4] + [1.34] * 2 + [4] * 9,
    ]
    assert skill_data.mods_at_max == [1.34] + [4] + [1.34] * 2 + [4] * 9
    assert skill_data.max_level == 2


def test_has_dummy_hits(transformer_skill: SkillTransformer):
    # Renee S1
    # https://dragalialost.gamepedia.com/Renee
    skill_data = transformer_skill.transform_attacking(103402031).with_conditions()

    assert skill_data.hit_count == [6, 6, 6, 6]
    assert skill_data.hit_count_at_max == 6
    assert skill_data.total_mod == pytest.approx([16.98, 17.82, 18.66, 18.78])
    assert skill_data.total_mod_at_max == pytest.approx(18.78)
    assert skill_data.mods == [[2.83] * 6, [2.97] * 6, [3.11] * 6, [3.13] * 6]
    assert skill_data.mods_at_max == [3.13] * 6
    assert skill_data.max_level == 4


def test_has_punisher_1_1(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica
    skill_data_base = transformer_skill.transform_attacking(107505011)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        2.69 * 3 + 3.37,
        2.99 * 3 + 3.73,
        3.32 * 3 + 4.15,
        5.97 * 3 + 6.86,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.97 * 3 + 6.86)
    assert skill_data.mods == [
        [2.69] * 3 + [3.37],
        [2.99] * 3 + [3.73],
        [3.32] * 3 + [4.15],
        [5.97] * 3 + [6.86],
    ]
    assert skill_data.mods_at_max == [5.97] * 3 + [6.86]
    assert skill_data.max_level == 4


def test_has_punisher_1_2(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica
    skill_data_base = transformer_skill.transform_attacking(107505011)

    # Poisoned Punisher
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_POISONED))

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        2.69 * 3 + 3.37,
        2.99 * 3 + 3.73,
        3.32 * 3 + 4.15,
        7.164 * 3 + 8.232,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(7.164 * 3 + 8.232)
    assert skill_data.mods == [
        [2.69] * 3 + [3.37],
        [2.99] * 3 + [3.73],
        [3.32] * 3 + [4.15],
        [7.164] * 3 + [8.232],
    ]
    assert skill_data.mods_at_max == [7.164] * 3 + [8.232]
    assert skill_data.max_level == 4


def test_has_punisher_2_1(transformer_skill: SkillTransformer):
    # Hawk S1
    # https://dragalialost.gamepedia.com/Hawk
    skill_data_base = transformer_skill.transform_attacking(106503021)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        7.69,
        8.07,
        8.48,
        4.74 * 2
    ])
    assert skill_data.total_mod_at_max == pytest.approx(4.74 * 2)
    assert skill_data.mods == [
        [7.69],
        [8.07],
        [8.48],
        [4.74] * 2
    ]
    assert skill_data.mods_at_max == [4.74] * 2
    assert skill_data.max_level == 4


def test_has_punisher_2_2(transformer_skill: SkillTransformer):
    # Hawk S1
    # https://dragalialost.gamepedia.com/Hawk
    skill_data_base = transformer_skill.transform_attacking(106503021)

    # Poisoned Punisher
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_POISONED))

    assert skill_data.hit_count == [1, 1, 1, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        7.69,
        8.07,
        8.48,
        4.74 + 14.22
    ])
    assert skill_data.total_mod_at_max == pytest.approx(4.74 + 14.22)
    assert skill_data.mods == [
        [7.69],
        [8.07],
        [8.48],
        [4.74, 14.22]
    ]
    assert skill_data.mods_at_max == [4.74, 14.22]
    assert skill_data.max_level == 4


def test_has_punisher_2_3(transformer_skill: SkillTransformer):
    # Hawk S1
    # https://dragalialost.gamepedia.com/Hawk
    skill_data_base = transformer_skill.transform_attacking(106503021)

    # Stunned Punisher
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_STUNNED))

    assert skill_data.hit_count == [1, 1, 1, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        7.69,
        16.7856,
        18.232,
        20.382 + 4.74
    ])
    assert skill_data.total_mod_at_max == pytest.approx(20.382 + 4.74)
    assert skill_data.mods == approx_matrix([
        [7.69],
        [16.7856],
        [18.232],
        [20.382, 4.74]
    ])
    assert skill_data.mods_at_max == [20.382, 4.74]
    assert skill_data.max_level == 4


def test_has_punisher_2_4(transformer_skill: SkillTransformer):
    # Hawk S1
    # https://dragalialost.gamepedia.com/Hawk
    skill_data_base = transformer_skill.transform_attacking(106503021)

    # Poisoned & Stunned Punisher
    skill_data = skill_data_base.with_conditions(
        SkillConditionComposite([SkillCondition.TARGET_STUNNED, SkillCondition.TARGET_POISONED]))

    assert skill_data.hit_count == [1, 1, 1, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        7.69,
        16.7856,
        18.232,
        20.382 + 14.22
    ])
    assert skill_data.total_mod_at_max == pytest.approx(20.382 + 14.22)
    assert skill_data.mods == approx_matrix([
        [7.69],
        [16.7856],
        [18.232],
        [20.382, 14.22]
    ])
    assert skill_data.mods_at_max == [20.382, 14.22]
    assert skill_data.max_level == 4


def test_has_punisher_3_1(transformer_skill: SkillTransformer):
    # Nefaria S1
    # https://dragalialost.gamepedia.com/Nefaria
    skill_data_base = transformer_skill.transform_attacking(106505011)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [8, 8, 8, 8]
    assert skill_data.hit_count_at_max == 8
    assert skill_data.total_mod == pytest.approx([
        1.036 * 8,
        1.09 * 8,
        1.144 * 8,
        1.144 * 8,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(1.144 * 8)
    assert skill_data.mods == [
        [1.036] * 8,
        [1.09] * 8,
        [1.144] * 8,
        [1.144] * 8,
    ]
    assert skill_data.mods_at_max == [1.144] * 8
    assert skill_data.max_level == 4


def test_has_punisher_3_2(transformer_skill: SkillTransformer):
    # Nefaria S1
    # https://dragalialost.gamepedia.com/Nefaria
    skill_data_base = transformer_skill.transform_attacking(106505011)

    # Blinded Punisher
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_BLINDED))

    assert skill_data.hit_count == [8, 8, 8, 8]
    assert skill_data.hit_count_at_max == 8
    assert skill_data.total_mod == pytest.approx([
        1.036 * 8,
        1.8421 * 8,
        1.99056 * 8,
        1.99056 * 8,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(1.99056 * 8)
    assert skill_data.mods == approx_matrix([
        [1.036] * 8,
        [1.8421] * 8,
        [1.99056] * 8,
        [1.99056] * 8,
    ])
    assert skill_data.mods_at_max == pytest.approx([1.99056] * 8)
    assert skill_data.max_level == 4


def test_has_punisher_3_3(transformer_skill: SkillTransformer):
    # Nefaria S1
    # https://dragalialost.gamepedia.com/Nefaria
    skill_data_base = transformer_skill.transform_attacking(106505011)

    # Poisoned Punisher
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_POISONED))

    assert skill_data.hit_count == [8, 8, 8, 8]
    assert skill_data.hit_count_at_max == 8
    assert skill_data.total_mod == pytest.approx([
        1.036 * 8,
        1.09 * 8,
        1.144 * 8,
        1.99056 * 8,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(1.99056 * 8)
    assert skill_data.mods == approx_matrix([
        [1.036] * 8,
        [1.09] * 8,
        [1.144] * 8,
        [1.99056] * 8,
    ])
    assert skill_data.mods_at_max == pytest.approx([1.99056] * 8)
    assert skill_data.max_level == 4


def test_has_punisher_3_4(transformer_skill: SkillTransformer):
    # Nefaria S1
    # https://dragalialost.gamepedia.com/Nefaria
    skill_data_base = transformer_skill.transform_attacking(106505011)

    # Blinded or Poisoned Punisher
    skill_data = skill_data_base.with_conditions(
        SkillConditionComposite([SkillCondition.TARGET_BLINDED, SkillCondition.TARGET_POISONED]))

    assert skill_data.hit_count == [8, 8, 8, 8]
    assert skill_data.hit_count_at_max == 8
    assert skill_data.total_mod == pytest.approx([
        1.036 * 8,
        1.8421 * 8,
        1.99056 * 8,
        1.99056 * 8,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(1.99056 * 8)
    assert skill_data.mods == approx_matrix([
        [1.036] * 8,
        [1.8421] * 8,
        [1.99056] * 8,
        [1.99056] * 8,
    ])
    assert skill_data.mods_at_max == pytest.approx([1.99056] * 8)
    assert skill_data.max_level == 4


def test_hp_related_1_1(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica
    skill_data_base = transformer_skill.transform_attacking(107505011)

    # 1 HP
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.SELF_HP_1))

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        6.0525 * 3 + 7.5825,
        6.7275 * 3 + 8.3925,
        7.47 * 3 + 9.3375,
        8.955 * 3 + 10.29,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(8.955 * 3 + 10.29)
    assert skill_data.mods == approx_matrix([
        [6.0525] * 3 + [7.5825],
        [6.7275] * 3 + [8.3925],
        [7.47] * 3 + [9.3375],
        [8.955] * 3 + [10.29],
    ])
    assert skill_data.mods_at_max == pytest.approx([8.955] * 3 + [10.29])
    assert skill_data.max_level == 4


def test_hp_related_1_2(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica
    skill_data_base = transformer_skill.transform_attacking(107505011)

    # 1 HP & Poisoned Punisher
    skill_data = skill_data_base.with_conditions(
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_1]))

    assert skill_data.hit_count == [4, 4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        6.0525 * 3 + 7.5825,
        6.7275 * 3 + 8.3925,
        7.47 * 3 + 9.3375,
        10.746 * 3 + 12.348,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(10.746 * 3 + 12.348)
    assert skill_data.mods == approx_matrix([
        [6.0525] * 3 + [7.5825],
        [6.7275] * 3 + [8.3925],
        [7.47] * 3 + [9.3375],
        [10.746] * 3 + [12.348],
    ])
    assert skill_data.mods_at_max == pytest.approx([10.746] * 3 + [12.348])
    assert skill_data.max_level == 4


def test_hp_related_2_1(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise
    skill_data_base = transformer_skill.transform_attacking(106503012)

    # Base data (Not given, default to full HP)
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([
        2.56 * 3,
        2.69 * 3,
        6.98 * 3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.98 * 3)
    assert skill_data.mods == approx_matrix([
        [2.56] * 3,
        [2.69] * 3,
        [6.98] * 3
    ])
    assert skill_data.mods_at_max == pytest.approx([6.98] * 3)
    assert skill_data.max_level == 3


def test_hp_related_2_2(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise
    skill_data_base = transformer_skill.transform_attacking(106503012)

    # Base data (Full HP)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.SELF_HP_FULL))

    assert skill_data.hit_count == [3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([
        2.56 * 3,
        2.69 * 3,
        6.98 * 3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.98 * 3)
    assert skill_data.mods == approx_matrix([
        [2.56] * 3,
        [2.69] * 3,
        [6.98] * 3
    ])
    assert skill_data.mods_at_max == pytest.approx([6.98] * 3)
    assert skill_data.max_level == 3


def test_hp_related_2_3(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise
    skill_data_base = transformer_skill.transform_attacking(106503012)

    # Poisoned Punisher (Full HP)
    skill_data = skill_data_base.with_conditions(
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_FULL]))

    assert skill_data.hit_count == [3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([
        3.456 * 3,
        4.035 * 3,
        10.47 * 3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(10.47 * 3)
    assert skill_data.mods == approx_matrix([
        [3.456] * 3,
        [4.035] * 3,
        [10.47] * 3
    ])
    assert skill_data.mods_at_max == pytest.approx([10.47] * 3)
    assert skill_data.max_level == 3


def test_hp_related_2_4(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise
    skill_data_base = transformer_skill.transform_attacking(106503012)

    # Base data (1 HP)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.SELF_HP_1))

    assert skill_data.hit_count == [3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([
        2.56 * 3,
        2.69 * 3,
        3.49 * 3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.49 * 3)
    assert skill_data.mods == approx_matrix([
        [2.56] * 3,
        [2.69] * 3,
        [3.49] * 3
    ])
    assert skill_data.mods_at_max == pytest.approx([3.49] * 3)
    assert skill_data.max_level == 3


def test_hp_related_2_5(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise
    skill_data_base = transformer_skill.transform_attacking(106503012)

    # Poisoned Punisher (1 HP)
    skill_data = skill_data_base.with_conditions(
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_1]))

    assert skill_data.hit_count == [3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([
        3.456 * 3,
        4.035 * 3,
        5.235 * 3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.235 * 3)
    assert skill_data.mods == approx_matrix([
        [3.456] * 3,
        [4.035] * 3,
        [5.235] * 3
    ])
    assert skill_data.mods_at_max == pytest.approx([5.235] * 3)
    assert skill_data.max_level == 3


def test_buff_related_1(transformer_skill: SkillTransformer):
    # Karina S1
    # https://dragalialost.gamepedia.com/Karina
    skill_data_base = transformer_skill.transform_attacking(104402011)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [2, 2, 2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([5.96 * 2, 6.63 * 2, 7.36 * 2, 8.18 * 2])
    assert skill_data.total_mod_at_max == pytest.approx(16.36)
    assert skill_data.mods == [[5.96] * 2, [6.63] * 2, [7.36] * 2, [8.18] * 2]
    assert skill_data.mods_at_max == [8.18] * 2
    assert skill_data.max_level == 4

    # With buffs
    condition_to_dmg_up_rate = {
        (SkillCondition.SELF_BUFF_0,): 1 + 0,
        (SkillCondition.SELF_BUFF_10,): 1 + 0.05 * 10,
        (SkillCondition.SELF_BUFF_20,): 1 + 0.05 * 20,
        (SkillCondition.SELF_BUFF_25,): 1 + 0.05 * 25,
        (SkillCondition.SELF_BUFF_30,): 1 + 0.05 * 30,
        (SkillCondition.SELF_BUFF_35,): 1 + 0.05 * 35,
        (SkillCondition.SELF_BUFF_40,): 1 + 0.05 * 40,
        (SkillCondition.SELF_BUFF_45,): 1 + 0.05 * 45,
        (SkillCondition.SELF_BUFF_50,): 1 + 0.05 * 50,
    }

    for conditions, boost_rate in condition_to_dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(SkillConditionComposite(conditions))

        assert skill_data.hit_count == [2, 2, 2, 2]
        assert skill_data.hit_count_at_max == 2
        assert skill_data.total_mod == pytest.approx([
            5.96 * 2 * boost_rate,
            6.63 * 2 * boost_rate,
            7.36 * 2 * boost_rate,
            8.18 * 2 * boost_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(8.18 * 2 * boost_rate)
        assert skill_data.mods == approx_matrix([
            [5.96 * boost_rate] * 2,
            [6.63 * boost_rate] * 2,
            [7.36 * boost_rate] * 2,
            [8.18 * boost_rate] * 2
        ])
        assert skill_data.mods_at_max == [8.18 * boost_rate] * 2
        assert skill_data.max_level == 4

# TEST: TBA - neutral additional skill damage (Cassandra, Lea S2)
