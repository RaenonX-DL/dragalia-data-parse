import pytest

from dlparse.enums import SkillNumber
from dlparse.mono.asset import SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_skill_discovery(asset_manager: AssetManager):
    # Undercover Grace
    # https://dragalialost.wiki/w/Undercover_Grace
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10150106)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(101501061, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(101501062, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # SS
        SkillIdEntry(101501063, SkillNumber.S1, SkillIdentifierLabel.SHARED),
    ]

    assert actual_identifiers == expected_identifiers


def test_s1(transformer_skill: SkillTransformer):
    # Undercover Grace S1
    # https://dragalialost.wiki/w/Undercover_Grace
    skill_data_base = transformer_skill.transform_attacking(101501061)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([
        17.82,
        19.80,
        22.00
    ])
    assert skill_data.total_mod_at_max == pytest.approx(22.00)
    assert skill_data.mods == approx_matrix([
        [17.82],
        [19.80],
        [22.00]
    ])
    assert skill_data.mods_at_max == pytest.approx([22.00])
    assert skill_data.max_level == 3
