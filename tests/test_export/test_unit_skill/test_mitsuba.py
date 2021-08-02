from dlparse.export.funcs.skill_atk import export_atk_skills
from dlparse.mono.manager import AssetManager


def test_export_skill_entries(asset_manager: AssetManager):
    skills, _ = export_atk_skills(
        asset_manager.asset_chara_data.get_data_by_id(10350202),
        asset_manager,
        skip_unparsable=False
    )

    # S1-1, S1-2
    assert {skill.skill_internal_id for skill in skills} == {103502021, 103502023}
