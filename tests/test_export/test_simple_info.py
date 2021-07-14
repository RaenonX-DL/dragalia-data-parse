import pytest

from dlparse.export import export_simple_info_as_entry_dict
from dlparse.export.entry import SimpleUnitInfoEntry
from dlparse.mono.manager import AssetManager
from tests.utils import is_json_schema_match


@pytest.mark.holistic
def test_exported_simple_info_json(asset_manager: AssetManager):
    entries = export_simple_info_as_entry_dict(asset_manager)

    for entry in entries.values():
        is_json_schema_match(SimpleUnitInfoEntry.json_schema, entry.to_json_entry())
