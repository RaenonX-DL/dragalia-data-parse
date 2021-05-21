import pytest

from dlparse.export import export_ex_abilities_as_entries
from dlparse.export.entry import CharaExAbiltiesEntry
from dlparse.mono.manager import AssetManager
from tests.utils import is_json_schema_match


@pytest.mark.holistic
def test_exported_json(asset_manager: AssetManager):
    entries = export_ex_abilities_as_entries(asset_manager)

    for entry in entries:
        is_json_schema_match(CharaExAbiltiesEntry.json_schema, entry.to_json_entry())
