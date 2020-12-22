from dlparse.enums import Condition, Language, cond_afflictions
from dlparse.export import export_condition_entries, export_enums_entries
from dlparse.export.funcs.enum_cond import condition_theme
from dlparse.mono.manager import AssetManager


def test_export_affliction_conditions(asset_manager: AssetManager):
    key = "affliction"

    entries = export_enums_entries(asset_manager, {key: cond_afflictions})

    assert len(entries) > 0

    conditions_missing: set[str] = {cond.name for cond in cond_afflictions}

    for entry in entries[key]:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans.text_dict
        assert Language.EN.value in entry.trans.text_dict
        assert Language.JP.value in entry.trans.text_dict

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"


def test_export_condition_enums(asset_manager: AssetManager):
    entries = export_condition_entries(asset_manager)

    assert len(entries) == len(Condition)

    for cond_code, entry in entries.items():
        condition = Condition(cond_code)

        if condition not in condition_theme:
            continue

        assert condition_theme[condition] == entry.color_theme
