import pytest

from dlparse.enums import Condition
from dlparse.errors import ActionDataNotFoundError, HitDataUnavailableError
from dlparse.model import SupportiveSkillEntry
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.expected_skills_lookup import skill_ids_sup


@pytest.mark.skip("Temporarily skipping exhaustive supportive skill transforming check. "
                  "Remove when start working on supportive skills.")
def test_transform_all_supportive_skills(
        transformer_skill: SkillTransformer, asset_manager: AssetManager
):
    skill_ids: list[int] = []
    for chara_data in asset_manager.asset_chara_data.playable_chara_data:
        skill_ids.extend([
            skill_entry.skill_id for skill_entry
            in chara_data.get_skill_id_entries(asset_manager)
        ])

    skill_ids_missing: dict[int, str] = skill_ids_sup.copy()
    skill_no_buff: set[tuple[int, tuple[Condition]]] = set()
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
