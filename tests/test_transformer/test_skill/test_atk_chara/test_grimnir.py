import pytest

from dlparse.enums import SkillNumber
from dlparse.mono.asset import SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_skill_discovery(asset_manager: AssetManager):
    # Vania
    # https://dragalialost.wiki/w/Vania
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10550304)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(105503041, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(105503042, SkillNumber.S2, [SkillIdentifierLabel.S2_BASE, SkillIdentifierLabel.SHARED]),
        # S1 @ Storm Lv.5
        SkillIdEntry(105503043, SkillNumber.S1, SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S1, 1925)),
    ]

    assert actual_identifiers == expected_identifiers


def test_s1(transformer_skill: SkillTransformer):
    # Grimnir S1 (Normal)
    # https://dragalialost.wiki/w/Grimnir
    skill_data_base = transformer_skill.transform_attacking(105503041)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        7.57 + 3 * 2.53,
        8.42 + 3 * 2.81,
        9.35 + 3 * 3.12
    ])
    assert skill_data.total_mod_at_max == pytest.approx(9.35 + 3 * 3.12)
    assert skill_data.mods == approx_matrix([
        [7.57] + 3 * [2.53],
        [8.42] + 3 * [2.81],
        [9.35] + 3 * [3.12]
    ])
    assert skill_data.mods_at_max == pytest.approx([9.35] + 3 * [3.12])
    assert skill_data.max_level == 3


def test_s1_storm_5(transformer_skill: SkillTransformer):
    # Grimnir S1 (Storm Lv.5)
    # https://dragalialost.wiki/w/Grimnir
    skill_data_base = transformer_skill.transform_attacking(105503043)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [10, 10, 10]
    assert skill_data.hit_count_at_max == 10
    assert skill_data.total_mod == pytest.approx([
        8 * 1.01 + 2 * 4.05,
        8 * 1.13 + 2 * 4.50,
        8 * 1.25 + 2 * 5.00,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(8 * 1.25 + 2 * 5.00)
    assert skill_data.mods == approx_matrix([
        8 * [1.01] + 2 * [4.05],
        8 * [1.13] + 2 * [4.50],
        8 * [1.25] + 2 * [5.00],
    ])
    assert skill_data.mods_at_max == pytest.approx(8 * [1.25] + 2 * [5.00])
    assert skill_data.max_level == 3


def test_s2(transformer_skill: SkillTransformer):
    # Grimnir S2
    # https://dragalialost.wiki/w/Grimnir
    skill_data_base = transformer_skill.transform_attacking(105503042)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [9, 9]
    assert skill_data.hit_count_at_max == 9
    assert skill_data.total_mod == pytest.approx([
        2.7 * 9,
        3.0 * 9,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.0 * 9)
    assert skill_data.mods == approx_matrix([
        [2.7] * 9,
        [3.0] * 9
    ])
    assert skill_data.mods_at_max == pytest.approx([3.0] * 9)
    assert skill_data.max_level == 2
