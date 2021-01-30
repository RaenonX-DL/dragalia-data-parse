from dlparse.enums import SkillNumber
from dlparse.mono.asset import SkillIdEntry, SkillIdentifierLabel
from dlparse.mono.manager import AssetManager


def test_chrom(asset_manager: AssetManager):
    # Chrom
    # https://dragalialost.wiki/w/Chrom
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10150105)

    actual_identifiers = chara_data.get_skill_id_entries(asset_manager)

    s2_1_stack_labels = [
        SkillIdentifierLabel.chrom_status_for_s2(1, 1),
        SkillIdentifierLabel.chrom_status_for_s2(1, 2),
        SkillIdentifierLabel.chrom_status_for_s2(1, 3)
    ]
    s2_2_stack_labels = [
        SkillIdentifierLabel.chrom_status_for_s2(2, 1),
        SkillIdentifierLabel.chrom_status_for_s2(2, 2),
        SkillIdentifierLabel.chrom_status_for_s2(2, 3)
    ]
    s2_2_stack_labels_not_3_gauges = [
        SkillIdentifierLabel.chrom_status_for_s2(3, 1),
        SkillIdentifierLabel.chrom_status_for_s2(3, 2)
    ]
    s1_2_plus_stacks = [
        SkillIdentifierLabel.chrom_status_for_s1(2),
        SkillIdentifierLabel.chrom_status_for_s1(3)
    ]

    expected_identifiers = [
        # S1 @ 0 Stack
        SkillIdEntry(101501051, SkillNumber.S1, SkillIdentifierLabel.chrom_status_for_s1(0)),
        # S2 @ 1 Stack
        SkillIdEntry(101501052, SkillNumber.S2, s2_1_stack_labels),
        # S2 @ 2 Stacks
        SkillIdEntry(101501053, SkillNumber.S2, s2_2_stack_labels),
        # S2 @ 3 Stacks (w/ 1 or 2 gauges)
        SkillIdEntry(101501054, SkillNumber.S2, s2_2_stack_labels_not_3_gauges),
        # S2 @ 3 Stacks (w/ 3 gauges)
        SkillIdEntry(101501055, SkillNumber.S2, SkillIdentifierLabel.chrom_status_for_s2(3, 3)),
        # S1 @ 1 Stack
        SkillIdEntry(101501056, SkillNumber.S1, SkillIdentifierLabel.chrom_status_for_s1(1)),
        # S1 @ 2+ Stack
        SkillIdEntry(101501057, SkillNumber.S1, s1_2_plus_stacks),
    ]

    assert actual_identifiers == expected_identifiers
