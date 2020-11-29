from dlparse.model import AttackingSkillDataEntry
from dlparse.mono.asset import CharaDataAsset, CharaDataEntry, CharaModeAsset, SkillDataAsset
from dlparse.transformer import SkillTransformer

skill_ids_atk: dict[int, str] = {
    # Normal tests
    101503021: "Wedding Elisanne S1",
    101503022: "Wedding Elisanne S2",
    101401012: "Euden S2",
    101403022: "Templar Hope S2",
    104502011: "Summer Julietta S1",
    104403011: "Ranzal S1",
    101504031: "Gala Euden S1",
    101504032: "Gala Euden S2",
    104402011: "Karina S1",
    107505011: "Yukata Curran S1",
    106503012: "Louise S2",
    101501022: "Marth S2",
    # Special tests
    105402011: "Elisanne S1",
    103505033: "Bellina S1 in enhanced mode",
    103505034: "Bellina S2 in enhanced mode",
    105502042: "Catherine S2 @ 0 Stacks / as SS",
    105502043: "Catherine S2 @ 1 Stack",
    105502044: "Catherine S2 @ 2 Stacks",
    105502045: "Catherine S2 @ 3 Stacks",
    105502046: "Catherine S2 @ as Helper",
}

skill_ids_sup: dict[int, str] = {
    # Normal tests
    105503022: "Kirsty S2",
    101503021: "Wedding Elisanne S1",
    105401031: "Emma S1",
    105405021: "Patia S1",
    101402012: "Halloween Odetta S2",
    104502012: "Summer Julietta S2 P1",
    104502013: "Summer Julietta S2 P2",
    104502014: "Summer Julietta S2 P3",
    106504012: "Summer Cleo S2",
    101501022: "Marth S2",
    # Special tests
    105402011: "Elisanne S1",
}


# TEST: Don't export skills that are not yet released (Templar hope S2 lv.3, Zena S2 lv.3)


def test_get_all_skill_ids(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset, asset_skill: SkillDataAsset):
    skill_ids = asset_chara.get_all_skill_ids(asset_chara_mode, skill_asset=asset_skill)

    for sid, note in skill_ids_atk.items():
        assert sid in skill_ids, f"Skill ID `{sid}` ({note}) not in the skill ID list (Attacking)"

    for sid, note in skill_ids_sup.items():
        assert sid in skill_ids, f"Skill ID `{sid}` ({note}) not in the skill ID list (Supportive)"


def test_transform_all_attack_skills(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset,
                                     asset_skill: SkillDataAsset, transformer_skill: SkillTransformer):
    skill_ids = asset_chara.get_all_skill_ids(asset_chara_mode, skill_asset=asset_skill)

    skill_ids_atk_missing: dict[int, str] = skill_ids_atk.copy()
    skill_ids_zero_mods: set[int] = set()
    skill_entries: list[AttackingSkillDataEntry] = []

    for skill_id in skill_ids:
        try:
            skill_data = transformer_skill.transform_attacking(skill_id)

            skill_entries.extend(skill_data.get_all_possible_entries())

            skill_ids_atk_missing.pop(skill_id, None)
            if not any(sum(mods_lv) > 0 for mods_lv in skill_data.mods):
                skill_ids_zero_mods.add(skill_id)
        except ValueError:
            # REMOVE: after all attacking skills can be parsed
            pass
        except FileNotFoundError as ex:
            print(f"Skill ID `{skill_id}` yielded file not found error:", ex)

    assert len(skill_entries) > 0

    assert len(skill_ids_atk_missing) == 0, \
        f"Missing attacking skills (could be more): {set(skill_ids_atk_missing.keys())}"
    assert len(skill_ids_zero_mods) == 0, \
        f"Skills without any modifiers included: {skill_ids_zero_mods}"


def test_get_catherine_skill_ids(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset,
                                 asset_skill: SkillDataAsset):
    # Catherine
    # https://dragalialost.gamepedia.com/Catherine

    skill_ids_expected = {
        105502041: "Catherine S1",
        105502042: "Catherine S2 @ 0 Stacks / as SS",
        105502043: "Catherine S2 @ 1 Stack",
        105502044: "Catherine S2 @ 2 Stacks",
        105502045: "Catherine S2 @ 3 Stacks",
        105502046: "Catherine S2 @ as Helper"
    }

    catherine: CharaDataEntry = asset_chara.get_data_by_id(10550204)
    catherine_skill_ids = {entry.skill_id for entry
                           in catherine.get_skill_identifiers(asset_chara_mode, skill_asset=asset_skill)}

    for skill_id in catherine_skill_ids:
        skill_ids_expected.pop(skill_id, None)

    assert \
        len(skill_ids_expected) == 0, \
        "\n".join(
            ["Missing Catherine skills:"]
            + [f"{skill_id:13} {note}" for skill_id, note in skill_ids_expected.items()]
        )
