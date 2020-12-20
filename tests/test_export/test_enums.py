from dlparse.enums import Language, cond_afflictions
from dlparse.export import export_enums_entries
from dlparse.mono.manager import AssetManager


def test_export_affliction_conditions(asset_manager: AssetManager):
    entries_affliction = export_enums_entries(asset_manager, cond_afflictions)

    assert len(entries_affliction) > 0

    conditions_missing: set[str] = {cond.name for cond in cond_afflictions}

    for entry in entries_affliction:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans
        assert Language.EN.value in entry.trans
        assert Language.JP.value in entry.trans

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"
