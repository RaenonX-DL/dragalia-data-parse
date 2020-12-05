import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.export import export_atk_skills_as_entries
from dlparse.mono.manager import AssetManager
from tests.expected_skills_lookup import skill_ids_atk

expected_contained_info: dict[tuple[int, SkillConditionComposite], pytest.approx] = {
    # Wedding Elisanne S2
    (101503022, SkillConditionComposite()): pytest.approx(10.515),
    # Euden S2
    (101401012, SkillConditionComposite()): pytest.approx(14.74),
    # Catherine S2 @ 3 Stacks
    (105502045, SkillConditionComposite()): pytest.approx(0.54 * 37 + 1.22 * 37),
    # Karina @ 50 Buffs
    (104402011, SkillConditionComposite(SkillCondition.SELF_BUFF_50)): pytest.approx(16.36 * (1 + 0.05 * 50)),
    # Veronica S1 @ 1 HP and target poisoned
    (107505011, SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_1])):
        pytest.approx(10.746 * 3 + 12.348)
}


def test_exported_entries(asset_manager: AssetManager):
    entries = export_atk_skills_as_entries(asset_manager)

    assert len(entries) > 0

    skill_ids_missing: dict[int, str] = skill_ids_atk.copy()

    for entry in entries:
        skill_ids_missing.pop(entry.skill_internal_id, None)

        key = (entry.skill_internal_id, entry.skill_condition_comp)

        if info := expected_contained_info.get(key):
            assert info == entry.skill_total_mods_max, f"Skill info mismatch: {key}"

    assert len(skill_ids_missing) == 0, f"Skill IDs missing: {skill_ids_missing}"
