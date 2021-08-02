import pytest

from dlparse.enums import SkillNumber
from dlparse.errors import HitDataUnavailableError
from dlparse.mono.asset import SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer


def test_s2_base(transformer_skill: SkillTransformer):
    # Gala Mascula - S2
    # https://dragalialost.wiki/w/Gala_Mascula
    with pytest.raises(HitDataUnavailableError):
        transformer_skill.transform_attacking(102502032)


def test_skill_discovery(asset_manager: AssetManager):
    # Gala Mascula
    # https://dragalialost.wiki/w/Gala_Mascula
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10250203)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(102502031, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(102502032, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 @ Master Control
        SkillIdEntry(102502033, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 94)),
        # S2 @ Master Control
        SkillIdEntry(
            102502034,
            SkillNumber.S2,
            [
                SkillIdentifierLabel.SHARED,
                SkillIdentifierLabel.of_mode(SkillNumber.S2, 94)
            ]
        ),
        # SS
        SkillIdEntry(102502035, SkillNumber.S1, SkillIdentifierLabel.HELPER),
    ]

    assert actual_identifiers == expected_identifiers
