from dlparse.enums import SkillNumber
from dlparse.mono.asset import CharaDataAsset, SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager
from .test_props import create_dummy


def test_dummy(asset_manager: AssetManager):
    chara_data = create_dummy(skill_1_id=103505031, skill_2_id=103505032)

    expected_identifiers = [
        SkillIdEntry(103505031, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(103505032, SkillNumber.S2, SkillIdentifierLabel.S2_BASE)
    ]

    assert chara_data.get_skill_id_entries(asset_manager) == expected_identifiers


def test_dummy_with_mode(asset_manager: AssetManager):
    chara_data = create_dummy(skill_1_id=103505031, skill_2_id=103505032, mode_2_id=12)

    expected_identifiers = [
        SkillIdEntry(103505031, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(103505032, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(103505033, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 12)),
        SkillIdEntry(103505034, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 12))
    ]

    assert chara_data.get_skill_id_entries(asset_manager) == expected_identifiers


def test_via_phase(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    # Summer Julietta S2
    # https://dragalialost.gamepedia.com/Summer_Julietta
    chara_data = asset_chara.get_data_by_id(10450201)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        SkillIdEntry(104502011, SkillNumber.S1, [SkillIdentifierLabel.S1_BASE, SkillIdentifierLabel.SHARED]),
        SkillIdEntry(104502012, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(104502013, SkillNumber.S2, SkillIdentifierLabel.of_phase(SkillNumber.S2, 2)),
        SkillIdEntry(104502014, SkillNumber.S2, SkillIdentifierLabel.of_phase(SkillNumber.S2, 3))
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

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    s1_labels_base = [
        SkillIdentifierLabel.S1_BASE,
        SkillIdentifierLabel.of_mode(SkillNumber.S1, 26),
        SkillIdentifierLabel.of_mode(SkillNumber.S1, 27),
        SkillIdentifierLabel.of_mode(SkillNumber.S1, 28),
        SkillIdentifierLabel.of_mode(SkillNumber.S1, 29)
    ]

    s2_labels_base = [
        SkillIdentifierLabel.S2_BASE,
        SkillIdentifierLabel.SHARED,
        SkillIdentifierLabel.of_mode(SkillNumber.S2, 26)
    ]

    expected_identifiers = [
        SkillIdEntry(105502041, SkillNumber.S1, s1_labels_base),
        SkillIdEntry(105502042, SkillNumber.S2, s2_labels_base),  # S2 @ 0 Stacks / SS
        SkillIdEntry(105502043, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 27)),  # S2 @ 1 Stack
        SkillIdEntry(105502044, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 28)),  # S2 @ 2 Stacks
        SkillIdEntry(105502045, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 29)),  # S2 @ 3 Stacks
        SkillIdEntry(105502046, SkillNumber.S1, SkillIdentifierLabel.HELPER)  # S2 as helper
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

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(104503011, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(104503012, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 @ Heaven's Breath
        SkillIdEntry(104503013, SkillNumber.S1,
                     SkillIdentifierLabel.skill_enhanced_by_skill(SkillNumber.S1, SkillNumber.S2)),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_enhancements_multi(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in action condition.

    Skill IDs can be found in the fields ``_EnhancedSkill1`` and ``_EnhancedSkill2`` of the action condition entries.
    """
    # Xander
    # https://dragalialost.gamepedia.com/Xander
    chara_data = asset_chara.get_data_by_id(10150201)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # SS
        SkillIdEntry(101502011, SkillNumber.S1, SkillIdentifierLabel.SHARED),
        # S2 Base
        SkillIdEntry(101502012, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 enhanced once (S1-P2)
        SkillIdEntry(101502013, SkillNumber.S1, SkillIdentifierLabel.of_phase(SkillNumber.S1, 2)),
        # S1 enhanced twice (S1-P3)
        SkillIdEntry(101502014, SkillNumber.S1, SkillIdentifierLabel.of_phase(SkillNumber.S1, 3)),
        # S1 Base
        SkillIdEntry(101502015, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_ability(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the ability data.

    These can be found from the ability variants of an ability data.
    """
    # Meene
    # https://dragalialost.gamepedia.com/Meene
    chara_data = asset_chara.get_data_by_id(10650303)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(106503031, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(106503032, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 @ 6+ butterflies
        SkillIdEntry(106503033, SkillNumber.S1, SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S1, 1268)),
        # S2 @ 6+ butterflies
        SkillIdEntry(106503036, SkillNumber.S2, SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S2, 1302)),
        # SS
        SkillIdEntry(106503037, SkillNumber.S1, SkillIdentifierLabel.SHARED),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_ability_2(asset_chara: CharaDataAsset, asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the ability data.

    These can be found from the ability variants of an ability data.
    """
    # Radiant Xuan Zang
    # https://dragalialost.gamepedia.com/Radiant_Xuan_Zang
    chara_data = asset_chara.get_data_by_id(10750403)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(107504031, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(107504032, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 @ CP = 100
        SkillIdEntry(107504033, SkillNumber.S1, SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S1, 963)),
        # S2 @ CP = 100
        SkillIdEntry(107504034, SkillNumber.S2, SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S2, 963)),
    ]

    assert actual_identifiers == expected_identifiers
