import pytest

from dlparse.errors import ActionDataNotFoundError, HitDataUnavailableError
from dlparse.model import AttackingSkillDataEntry
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.expected_skills_lookup import skill_ids_atk

allowed_no_base_mods_sid = {
    103505042,  # Nevin S2, only has mods when sigil released or unlocked
    109503012,  # Formal Joachim S2, only has poisoning effect
    105401022,  # Xuan Zang S2, only debuff the enemy
    105404022,  # Sha Wujing S2, only debuff the enemy
    107501042,  # Seimei S2, only has mods when Shikigami is summoned
    109505012,  # Gala Chelle S2, only debuff (ATK down) the enemy
    299000112,  # Panther S2, placeholder dragon skill
}


@pytest.mark.holistic
def test_transform_all_attack_skills(transformer_skill: SkillTransformer, asset_manager: AssetManager):
    skill_ids: list[int] = []
    for chara_data in asset_manager.asset_chara_data.playable_data:
        skill_ids.extend([
            skill_entry.skill_id for skill_entry
            in chara_data.get_skill_id_entries(asset_manager)
        ])

    skill_ids_missing: dict[int, str] = skill_ids_atk.copy()
    skill_ids_zero_mods: set[int] = set()
    skill_entries: list[AttackingSkillDataEntry] = []

    for skill_id in skill_ids:
        try:
            skill_data = transformer_skill.transform_attacking(skill_id)

            skill_entries.extend(skill_data.get_all_possible_entries())

            skill_ids_missing.pop(skill_id, None)
            if not skill_data.has_non_zero_mods:
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
