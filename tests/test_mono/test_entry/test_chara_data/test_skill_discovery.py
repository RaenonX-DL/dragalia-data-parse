from dlparse.enums import ModeChangeType, SkillChainCondition, SkillNumber
from dlparse.mono.asset import SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager
from .utils import create_dummy


def test_dummy(asset_manager: AssetManager):
    chara_data = create_dummy(skill_1_id=103505031, skill_2_id=103505032)

    expected_identifiers = [
        SkillIdEntry(103505031, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        SkillIdEntry(103505032, SkillNumber.S2, SkillIdentifierLabel.S2_BASE)
    ]

    assert chara_data.get_skill_id_entries(asset_manager) == expected_identifiers


def test_dummy_with_mode_change_on_start(asset_manager: AssetManager):
    chara_data = create_dummy(
        skill_1_id=103505031, skill_2_id=103505032,
        mode_change_type=ModeChangeType.BUTTON, mode_2_id=12
    )

    expected_identifiers = [
        SkillIdEntry(103505033, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 12)),
        SkillIdEntry(103505034, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 12))
    ]

    assert chara_data.get_skill_id_entries(asset_manager) == expected_identifiers


def test_via_phase(asset_manager: AssetManager):
    # Summer Julietta S2
    # https://dragalialost.wiki/w/Summer_Julietta
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10450201)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        SkillIdEntry(104502011, SkillNumber.S1, [SkillIdentifierLabel.S1_BASE, SkillIdentifierLabel.SHARED]),
        SkillIdEntry(104502012, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        SkillIdEntry(104502013, SkillNumber.S2, SkillIdentifierLabel.of_phase(SkillNumber.S2, 2)),
        SkillIdEntry(104502014, SkillNumber.S2, SkillIdentifierLabel.of_phase(SkillNumber.S2, 3))
    ]

    assert actual_identifiers == expected_identifiers


def test_via_mode_1(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in chara mode data asset.

    Skill IDs can be found in the fields ``_Skill1Id`` and ``_Skill2Id`` of the chara mode data entries.
    """
    # Catherine
    # https://dragalialost.wiki/w/Catherine
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10550204)

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

    assert expected_identifiers == actual_identifiers


def test_via_mode_2(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in chara mode data asset.

    Skill IDs can be found in the fields ``_Skill1Id`` and ``_Skill2Id`` of the chara mode data entries.
    """
    # Gala Leif
    # https://dragalialost.wiki/w/Gala_Leif
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10150303)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        SkillIdEntry(101503031, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 22)),
        SkillIdEntry(101503032, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 22)),
        SkillIdEntry(101503033, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 23)),
        SkillIdEntry(101503034, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 23)),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_mode_3(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in chara mode data asset.

    Skill IDs can be found in the fields ``_Skill1Id`` and ``_Skill2Id`` of the chara mode data entries.
    """
    # Valerio
    # https://dragalialost.wiki/w/Valerio
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10250201)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        SkillIdEntry(102502011, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 4)),
        SkillIdEntry(102502012, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 4)),
        SkillIdEntry(102502013, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 5)),
        SkillIdEntry(102502014, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, 6)),
        SkillIdEntry(102502015, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 5)),
        SkillIdEntry(102502016, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, 6))
    ]

    assert actual_identifiers == expected_identifiers


def test_via_enhancements(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in action condition.

    Skill IDs can be found in the fields ``_EnhancedSkill1`` and ``_EnhancedSkill2`` of the action condition entries.
    """
    # Lin You
    # https://dragalialost.wiki/w/Lin_You
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10450301)

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


def test_via_enhancements_multi(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in action condition.

    Skill IDs can be found in the fields ``_EnhancedSkill1`` and ``_EnhancedSkill2`` of the action condition entries.
    """
    # Xander
    # https://dragalialost.wiki/w/Xander
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10150201)

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


def test_via_enhancements_multi_action(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in action condition.

    Skill IDs can be found in the fields ``_EnhancedSkill1`` and ``_EnhancedSkill2`` of the action condition entries.

    Additionally, this checks if all possible skill actions are returned.
    For example, Nadine S2 randomly picks one effect, both of these should be returned.
    """
    # Nadine
    # https://dragalialost.wiki/w/Nadine
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10550102)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    label_s1_enhanced_by_s2 = SkillIdentifierLabel.skill_enhanced_by_skill(SkillNumber.S1, SkillNumber.S2)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(105501021, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base - 1
        SkillIdEntry(105501022, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 enhanced by S2
        SkillIdEntry(105501023, SkillNumber.S1, label_s1_enhanced_by_s2),
        # SS variant
        SkillIdEntry(105501025, SkillNumber.S1, SkillIdentifierLabel.SHARED),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_ability(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the ability data.

    These can be found from the ability variants of an ability data.
    """
    # Meene
    # https://dragalialost.wiki/w/Meene
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10650303)

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


def test_via_ability_2(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the ability data.

    These can be found from the ability variants of an ability data.
    """
    # Radiant Xuan Zang
    # https://dragalialost.wiki/w/Radiant_Xuan_Zang
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10750403)

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


def test_via_ability_3(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the ability data.

    These can be found from the ability variants of an ability data.
    """
    # Yaten
    # https://dragalialost.wiki/w/Yaten
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10150501)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(101505011, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(101505012, SkillNumber.S2, [SkillIdentifierLabel.S2_BASE, SkillIdentifierLabel.SHARED]),
        # S1 @ Energized
        SkillIdEntry(101505013, SkillNumber.S1, SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S1, 2262)),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_ability_4(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the ability data.

    These can be found from the ability variants of an ability data.
    """
    # Original Maribelle
    # https://dragalialost.wiki/w/Maribelle
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10750301)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(107503011, SkillNumber.S1, [SkillIdentifierLabel.S1_BASE, SkillIdentifierLabel.SHARED]),
        # S2 Base
        SkillIdEntry(107503012, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S2 @ Energized
        SkillIdEntry(107503013, SkillNumber.S2, SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S2, 1398)),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_chain(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are buried in the skill chain data.

    These can be found from the ability variants of an ability data.
    """
    # Gala Alex
    # https://dragalialost.wiki/w/Gala_Alex
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10150502)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(101505021, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(101505022, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 Chained
        SkillIdEntry(101505023, SkillNumber.S1,
                     SkillIdentifierLabel.of_chain(SkillNumber.S1, SkillChainCondition.NONE)),
        # S1 Chained (Target buffed)
        SkillIdEntry(101505024, SkillNumber.S1,
                     SkillIdentifierLabel.of_chain(SkillNumber.S1, SkillChainCondition.TARGET_HAS_BUFF)),
        # S1 Chained (Target break)
        SkillIdEntry(101505025, SkillNumber.S1,
                     SkillIdentifierLabel.of_chain(SkillNumber.S1, SkillChainCondition.TARGET_BK_STATE)),
        # S2 Chained
        SkillIdEntry(101505026, SkillNumber.S2,
                     SkillIdentifierLabel.of_chain(SkillNumber.S2, SkillChainCondition.NONE)),
        # S2 Chained (Target buffed)
        SkillIdEntry(101505027, SkillNumber.S2,
                     SkillIdentifierLabel.of_chain(SkillNumber.S2, SkillChainCondition.TARGET_HAS_BUFF)),
        # S2 Chained (Target break)
        SkillIdEntry(101505028, SkillNumber.S2,
                     SkillIdentifierLabel.of_chain(SkillNumber.S2, SkillChainCondition.TARGET_BK_STATE)),
    ]

    assert actual_identifiers == expected_identifiers


def test_via_unique_dragon(asset_manager: AssetManager):
    """
    Get the skill IDs which variants are in the form of dragon skill (character has unique dragon).

    These can be found from the unique dragon linked to the character data.
    """
    # Tiki
    # https://dragalialost.wiki/w/Tiki
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10350203)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    expected_identifiers = [
        # S1 Base
        SkillIdEntry(103502031, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
        # S2 Base
        SkillIdEntry(103502032, SkillNumber.S2, SkillIdentifierLabel.S2_BASE),
        # S1 in unique dragon
        SkillIdEntry(299000061, SkillNumber.S1_DRAGON, SkillIdentifierLabel.S1_DRAGON),
        # S2 in unique dragon
        SkillIdEntry(299000062, SkillNumber.S2_DRAGON, SkillIdentifierLabel.S2_DRAGON),
    ]

    assert actual_identifiers == expected_identifiers
