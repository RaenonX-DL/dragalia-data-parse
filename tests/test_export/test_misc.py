import pytest

from dlparse.export import export_atk_skills_as_entries
from dlparse.mono.asset import CharaDataAsset, CharaModeAsset, TextAsset
from dlparse.transformer import SkillTransformer

skill_max_lv: dict[int, tuple[int, str]] = {
    101403022: (2, "Templar Hope S2"),
    107505042: (2, "OG Zena S2")
}

unplayable_chara_ids: list[int] = [
    19900001,
    19900002,
    30130102,
    30350201,
    30430301,
    99130001,
    99230001,
    99330001,
    99430001,
    99530001,
    99630001,
    99730001,
    99830001,
    99930001,
]


def test_max_lv(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset, asset_text: TextAsset,
                transformer_skill: SkillTransformer):
    entries = export_atk_skills_as_entries(asset_chara, asset_chara_mode, asset_text, transformer_skill,
                                           skip_unparsable=True)

    for entry in entries:
        if test_entry := skill_max_lv.get(entry.skill_internal_id):
            max_lv, description = test_entry

            if max_lv != entry.skill_max_level:
                pytest.fail(f"Max level of {description} mismatch. "
                            f"Expected: {max_lv} / Actual: {entry.skill_max_level}")


def test_no_unplayable(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset, asset_text: TextAsset,
                       transformer_skill: SkillTransformer):
    entries = export_atk_skills_as_entries(asset_chara, asset_chara_mode, asset_text, transformer_skill,
                                           skip_unparsable=True)

    for entry in entries:
        if entry.character_internal_id in unplayable_chara_ids:
            pytest.fail(f"Unplayable character included: {entry.character_internal_id}")
