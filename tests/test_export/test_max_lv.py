import pytest

from dlparse.export import export_atk_skills_as_entries
from dlparse.mono.asset import CharaDataAsset, CharaModeAsset, TextAsset
from dlparse.transformer import SkillTransformer

skill_max_lv: dict[int, tuple[int, str]] = {
    101403022: (2, "Templar Hope S2"),
    107505042: (2, "OG Zena S2")
}


def test_max_lv(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset, asset_text: TextAsset,
                transformer_skill: SkillTransformer):
    entries = export_atk_skills_as_entries(asset_chara, asset_chara_mode, asset_text, transformer_skill, True)

    for entry in entries:
        if test_entry := skill_max_lv.get(entry.skill_internal_id):
            max_lv, description = test_entry

            if max_lv != entry.skill_max_lv:
                pytest.fail(f"Max level of {description} mismatch. Expected: {max_lv} / Actual: {entry.skill_max_lv}")
