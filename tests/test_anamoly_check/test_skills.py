from dlparse.model import AttackingSkillDataEntry
from dlparse.mono.asset import CharaDataAsset, CharaModeAsset
from dlparse.transformer import SkillTransformer


def test_get_all_skill_ids(asset_chara_data: CharaDataAsset, asset_chara_mode: CharaModeAsset):
    skill_ids_should_be_included = [
        ((103505033, 103505034), "Bellina S1 / S2 in enhanced mode")
    ]

    skill_ids = asset_chara_data.get_all_skill_ids(asset_chara_mode)

    for sids_should_be_included, note in skill_ids_should_be_included:
        for sid in sids_should_be_included:
            assert sid in skill_ids, f"Skill ID `{sid}` ({note}) not in the skill ID list"


def test_transform_all_attack_skills(asset_chara_data: CharaDataAsset, asset_chara_mode: CharaModeAsset,
                                     transformer_skill: SkillTransformer):
    skill_ids = asset_chara_data.get_all_skill_ids(asset_chara_mode)

    skill_entries: list[AttackingSkillDataEntry] = []

    for skill_id in skill_ids:
        try:
            skill_entries.extend(transformer_skill.transform_attacking(skill_id).get_all_possible_entries())
        except ValueError:
            pass
        except FileNotFoundError as ex:
            print(f"Skill ID `{skill_id}` yielded file not found error:", ex)

    assert len(skill_entries) > 0
