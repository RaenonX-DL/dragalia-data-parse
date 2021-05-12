import pytest

from dlparse.enums import SkillNumber
from dlparse.mono.asset import SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_skill_discovery(asset_manager: AssetManager):
    # Vania
    # https://dragalialost.wiki/w/Vania
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10750505)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(107505051, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(107505052, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 @ Blood Pacts Lv.5
        SkillIdEntry(107505053, SkillNumber.S1, [
            SkillIdentifierLabel.SHARED,
            SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S1, 1931),
            SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S1, 1933)
        ]),
    ]

    assert actual_identifiers == expected_identifiers


def test_s1(transformer_skill: SkillTransformer):
    # Vania S1 (Normal)
    # https://dragalialost.wiki/w/Vania
    skill_data_base = transformer_skill.transform_attacking(107505051)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        3 * 4.22 + 5.31,
        3 * 4.52 + 5.67,
        3 * 5.23 + 6.44
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3 * 5.23 + 6.44)
    assert skill_data.mods == approx_matrix([
        3 * [4.22] + [5.31],
        3 * [4.52] + [5.67],
        3 * [5.23] + [6.44]
    ])
    assert skill_data.mods_at_max == pytest.approx(3 * [5.23] + [6.44])
    assert skill_data.max_level == 3


def test_s1_blood_pacts_5(transformer_skill: SkillTransformer):
    # Vania S1 (Blood Pacts Lv.5)
    # https://dragalialost.wiki/w/Vania
    skill_data_base = transformer_skill.transform_attacking(107505053)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        3 * 4.44 + 8.56,
        3 * 4.75 + 9.15,
        3 * 5.50 + 10.4
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3 * 5.50 + 10.4)
    assert skill_data.mods == approx_matrix([
        3 * [4.44] + [8.56],
        3 * [4.75] + [9.15],
        3 * [5.50] + [10.4]
    ])
    assert skill_data.mods_at_max == pytest.approx(3 * [5.50] + [10.4])
    assert skill_data.max_level == 3
