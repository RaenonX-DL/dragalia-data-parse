from dlparse.mono.asset import CharaDataAsset, SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager
from .test_props import create_dummy


def test_dummy(asset_manager: AssetManager):
    entry = create_dummy(skill_1_id=103505031, skill_2_id=103505032)

    expected_identifiers = [
        SkillIdEntry(103505031, 1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(103505032, 2, SkillIdentifierLabel.S2_BASE)
    ]

    assert entry.get_skill_identifiers(asset_manager) == expected_identifiers


def test_dummy_with_mode(asset_manager: AssetManager):
    entry = create_dummy(skill_1_id=103505031, skill_2_id=103505032, mode_2_id=12)

    expected_identifiers = [
        SkillIdEntry(103505031, 1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(103505032, 2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(103505033, 1, SkillIdentifierLabel.of_mode(1, 12)),
        SkillIdEntry(103505034, 2, SkillIdentifierLabel.of_mode(2, 12))
    ]

    assert entry.get_skill_identifiers(asset_manager) == expected_identifiers


def test_via_phase(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    # Summer Julietta S2
    # https://dragalialost.gamepedia.com/Summer_Julietta
    chara_data = asset_chara.get_data_by_id(10450201)

    actual_identifiers = chara_data.get_skill_identifiers(asset_manager)

    expected_identifiers = [
        SkillIdEntry(104502011, 1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(104502012, 2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(104502013, 2, SkillIdentifierLabel.of_phase(2, 2)),
        SkillIdEntry(104502014, 2, SkillIdentifierLabel.of_phase(2, 3))
    ]

    assert actual_identifiers == expected_identifiers


def test_via_mode(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in chara mode data asset.

    Skill IDs can be found in the fields ``_Skill1Id`` and ``_Skill2Id`` of the chara mode data entries.
    """
    # Catherine
    # https://dragalialost.gamepedia.com/Catherine
    chara_data = asset_chara.get_data_by_id(10550204)

    actual_identifiers = chara_data.get_skill_identifiers(asset_manager)

    expected_identifiers = [
        SkillIdEntry(105502041, 1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(105502042, 2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(105502041, 1, SkillIdentifierLabel.of_mode(1, 26)),
        SkillIdEntry(105502042, 2, SkillIdentifierLabel.of_mode(2, 26)),  # S2 @ 0 Stacks / SS
        SkillIdEntry(105502041, 1, SkillIdentifierLabel.of_mode(1, 27)),
        SkillIdEntry(105502043, 2, SkillIdentifierLabel.of_mode(2, 27)),  # S2 @ 1 Stack
        SkillIdEntry(105502041, 1, SkillIdentifierLabel.of_mode(1, 28)),
        SkillIdEntry(105502044, 2, SkillIdentifierLabel.of_mode(2, 28)),  # S2 @ 2 Stacks
        SkillIdEntry(105502041, 1, SkillIdentifierLabel.of_mode(1, 29)),
        SkillIdEntry(105502045, 2, SkillIdentifierLabel.of_mode(2, 29)),  # S2 @ 3 Stacks
        SkillIdEntry(105502046, 1, SkillIdentifierLabel.HELPER)  # S2 as helper
    ]

    assert actual_identifiers == expected_identifiers


def test_via_enhancements(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in action condition.

    Skill IDs can be found in the fields ``_EnhancedSkill1`` and ``_EnhancedSkill2`` of the action condition entries.
    """
    # Lin You
    # https://dragalialost.gamepedia.com/Lin_You
    chara_data = asset_chara.get_data_by_id(10450301)

    actual_identifiers = chara_data.get_skill_identifiers(asset_manager)

    expected_identifiers = [
        SkillIdEntry(104503011, 1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(104503012, 2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(104503013, 1, SkillIdentifierLabel.skill_enhanced_by_skill(1, 2)),  # S1 @ Heaven's Breath
    ]

    assert actual_identifiers == expected_identifiers


def test_via_ability(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the ability data.

    These can be found from the ability data b
    """
    # Meene
    # https://dragalialost.gamepedia.com/Meene
    chara_data = asset_chara.get_data_by_id(10650303)

    actual_identifiers = chara_data.get_skill_identifiers(asset_manager)

    expected_identifiers = [
        SkillIdEntry(106503031, 1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(106503032, 2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(106503033, 1, SkillIdentifierLabel.skill_enhanced_by_ability(1, 1268)),  # S1 @ 6+ butterflies
        SkillIdEntry(106503036, 2, SkillIdentifierLabel.skill_enhanced_by_ability(2, 1302)),  # S2 @ 6+ butterflies
    ]

    assert actual_identifiers == expected_identifiers
