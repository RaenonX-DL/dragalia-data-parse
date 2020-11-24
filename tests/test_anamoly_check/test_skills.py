from dlparse.model import AttackingSkillDataEntry
from dlparse.mono.asset import CharaDataAsset, CharaDataEntry, CharaModeAsset, SkillDataAsset
from dlparse.transformer import SkillTransformer

skill_ids_atk: dict[int, str] = {
    103505033: "Bellina S1 in enhanced mode",
    103505034: "Bellina S2 in enhanced mode",
    105502042: "Catherine S2 @ 0 Stacks / as SS",
    105502043: "Catherine S2 @ 1 Stack",
    105502044: "Catherine S2 @ 2 Stacks",
    105502045: "Catherine S2 @ 3 Stacks",
    105502046: "Catherine S2 @ as Helper"
}


def test_get_all_skill_ids(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset, asset_skill: SkillDataAsset):
    skill_ids = asset_chara.get_all_skill_ids(asset_chara_mode, skill_asset=asset_skill)

    for sid, note in skill_ids_atk.items():
        assert sid in skill_ids, f"Skill ID `{sid}` ({note}) not in the skill ID list"


def test_transform_all_attack_skills(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset,
                                     asset_skill: SkillDataAsset, transformer_skill: SkillTransformer):
    skill_ids = asset_chara.get_all_skill_ids(asset_chara_mode, skill_asset=asset_skill)

    skill_ids_atk_missing: dict[int, str] = skill_ids_atk.copy()
    skill_entries: list[AttackingSkillDataEntry] = []

    for skill_id in skill_ids:
        try:
            skill_entries.extend(transformer_skill.transform_attacking(skill_id).get_all_possible_entries())

            if skill_id in skill_ids_atk_missing:  # Not all skills listed, popping these emits :class:`KeyError`
                skill_ids_atk_missing.pop(skill_id)
        except ValueError:
            # REMOVE: after all attacking skills can be parsed
            pass
        except FileNotFoundError as ex:
            print(f"Skill ID `{skill_id}` yielded file not found error:", ex)

    assert len(skill_entries) > 0
    assert \
        len(skill_ids_atk_missing) == 0, \
        "\n".join(
            ["Missing attacking skills (could be more): "]
            + [f"{sid:13} {name}" for sid, name in skill_ids_atk_missing.items()]
        )


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
    catherine_skill_ids = {skill_id for skill_id, _, _
                           in catherine.get_skill_identifiers(asset_chara_mode, skill_asset=asset_skill)}

    for skill_id in catherine_skill_ids:
        skill_ids_expected.pop(skill_id, None)

    assert \
        len(skill_ids_expected) == 0, \
        "\n".join(
            ["Missing Catherine skills:"]
            + [f"{skill_id:13} {note}" for skill_id, note in skill_ids_expected.items()]
        )
