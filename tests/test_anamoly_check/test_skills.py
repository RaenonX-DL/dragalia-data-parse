import pytest

from dlparse.enums import SkillCondition
from dlparse.errors import ActionDataNotFoundError, HitDataUnavailableError
from dlparse.model import AttackingSkillDataEntry, SupportiveSkillEntry
from dlparse.mono.asset import CharaDataAsset, CharaDataEntry
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.expected_skills_lookup import skill_ids_atk, skill_ids_sup

allowed_no_base_mods_sid = {
    103505042,  # Nevin S2, only has either sigil released or unlocked
    109503012  # Formal Joachim S2, only poison
}


def test_transform_all_attack_skills(
        asset_chara: CharaDataAsset, transformer_skill: SkillTransformer, asset_manager: AssetManager
):
    skill_ids: list[int] = []
    for chara_data in asset_chara:
        chara_data: CharaDataEntry

        if not chara_data.is_playable:
            continue  # Don't care about non-playable units

        skill_ids.extend([
            skill_entry.skill_id for skill_entry
            in chara_data.get_skill_identifiers(asset_manager)
        ])

    skill_ids_missing: dict[int, str] = skill_ids_atk.copy()
    skill_ids_zero_mods: set[int] = set()
    skill_entries: list[AttackingSkillDataEntry] = []

    for skill_id in skill_ids:
        try:
            skill_data = transformer_skill.transform_attacking(skill_id)

            skill_entries.extend(skill_data.get_all_possible_entries())

            skill_ids_missing.pop(skill_id, None)
            if not any(sum(mods_lv) > 0 for mods_lv in skill_data.mods):
                skill_ids_zero_mods.add(skill_id)
        except HitDataUnavailableError:
            # No attacking data found / skill is not an attacking skill
            pass
        except ActionDataNotFoundError:
            # Action ID found for higher level, but no related action data found yet
            pass

    assert len(skill_entries) > 0

    assert len(skill_ids_missing) == 0, f"Missing attacking skills (could be more): {set(skill_ids_missing.keys())}"

    no_base_mods_sid = skill_ids_zero_mods - allowed_no_base_mods_sid
    assert len(no_base_mods_sid) == 0, f"Skills without any modifiers included: {no_base_mods_sid}"


@pytest.mark.skip("Temporarily skipping total supportive skill transforming check. "
                  "Remove when start working on supportive skills.")
def test_transform_all_supportive_skills(
        asset_chara: CharaDataAsset, transformer_skill: SkillTransformer, asset_manager: AssetManager
):
    skill_ids: list[int] = []
    for chara_data in asset_chara:
        chara_data: CharaDataEntry

        if not chara_data.is_playable:
            continue  # Don't care about non-playable units

        skill_ids.extend([skill_entry.skill_id
                          for skill_entry
                          in chara_data.get_skill_identifiers(asset_manager)])

    skill_ids_missing: dict[int, str] = skill_ids_sup.copy()
    skill_no_buff: set[tuple[int, tuple[SkillCondition]]] = set()
    skill_entries: list[SupportiveSkillEntry] = []

    for skill_id in skill_ids:
        try:
            skill_data = transformer_skill.transform_supportive(skill_id)

            entries = skill_data.get_all_possible_entries()

            skill_entries.extend(entries)

            skill_ids_missing.pop(skill_id, None)
            for entry in entries:
                if not any(entry.buffs):
                    skill_no_buff.add((skill_id, entry.condition_comp.conditions_sorted))
        except HitDataUnavailableError:
            # No attacking data found / skill is not an attacking skill
            pass
        except ActionDataNotFoundError:
            # Action ID found for higher level, but no related action data found yet
            pass

    assert len(skill_entries) > 0

    assert len(skill_ids_missing) == 0, f"Missing attacking skills (could be more): {set(skill_ids_missing.keys())}"
    assert len(skill_no_buff) == 0, f"Skills without any buffs: {skill_no_buff}"
