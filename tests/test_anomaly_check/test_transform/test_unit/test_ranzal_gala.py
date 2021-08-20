from dlparse.enums import Condition, ConditionComposite
from dlparse.export.funcs.skill_atk import export_atk_skills
from dlparse.mono.manager import AssetManager


def test_export_s1(asset_manager: AssetManager):
    unit_data = asset_manager.asset_chara_data.get_data_by_id(10150301)

    skill_entry, _ = export_atk_skills(unit_data, asset_manager, skip_unparsable=False)

    skill_entry_2_gauges = next(
        (entry for entry in skill_entry if entry.condition_comp == ConditionComposite(Condition.SELF_GAUGE_FILLED_2)),
        None
    )
    # 6 hits w/ each hit dealing 309%, boosted by 2x by ability
    assert skill_entry_2_gauges.skill_total_mods_max == 3.09 * 6 * 2
