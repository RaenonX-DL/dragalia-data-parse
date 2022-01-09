from typing import Any

import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.export import export_atk_skills_as_entries
from dlparse.export.entry import AttackingSkillEntry
from dlparse.mono.manager import AssetManager
from tests.expected_skills_lookup import skill_ids_atk
from tests.utils import is_json_schema_match

expected_contained_info: dict[tuple[int, ConditionComposite], pytest.approx] = {
    # Wedding Elisanne S2
    (101503022, ConditionComposite()): pytest.approx(10.515),
    # Euden S2
    (101401012, ConditionComposite()): pytest.approx(14.74),
    # Catherine S2 @ 3 Stacks
    (105502045, ConditionComposite()): pytest.approx(0.6 * 37 + 1.3 * 37),
    # Yoshitsune S1 @ Not countered
    (109502021, ConditionComposite()): pytest.approx(10.65),
    # Yoshitsune S1 @ Countered
    (109502021, ConditionComposite(Condition.COUNTER_RED_ATTACK)): pytest.approx(26.47)
}


@pytest.mark.holistic
def test_exported_entries(asset_manager: AssetManager):
    entries = export_atk_skills_as_entries(asset_manager, skip_unparsable=False)

    assert len(entries) > 0

    skill_ids_missing: dict[int, str] = skill_ids_atk.copy()
    # `Any` should be the type of approx, but the API hasn't exposed: https://github.com/pytest-dev/pytest/issues/7469
    skill_comp_missing: dict[tuple[int, ConditionComposite], Any] = expected_contained_info.copy()

    for entry in entries:
        key = (entry.skill_internal_id, entry.condition_comp)

        skill_ids_missing.pop(entry.skill_internal_id, None)
        skill_comp_missing.pop(key, None)

        if info := expected_contained_info.get(key):
            assert info == entry.skill_total_mods_max, f"Skill info mismatch: {key}"

    assert len(skill_ids_missing) == 0, f"Skill IDs missing: {skill_ids_missing}"
    assert len(skill_comp_missing) == 0, f"Skill composition missing: {skill_comp_missing}"


@pytest.mark.holistic
def test_exported_json(asset_manager: AssetManager):
    entries = export_atk_skills_as_entries(asset_manager)

    for entry in entries:
        is_json_schema_match(AttackingSkillEntry.json_schema, entry.to_json_entry())
