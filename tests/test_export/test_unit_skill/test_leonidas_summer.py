from dlparse.export.funcs.skill_atk import export_atk_skills
from dlparse.mono.manager import AssetManager


def test_export_skill_entries(asset_manager: AssetManager):
    skills, _ = export_atk_skills(
        asset_manager.asset_chara_data.get_data_by_id(10550503),
        asset_manager,
        skip_unparsable=False
    )

    # S1, S1E, S2
    assert len(skills) == 3
