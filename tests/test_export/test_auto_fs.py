import pytest

from dlparse.export import export_auto_fs_info_as_entry_dict
from dlparse.export.entry import AutoFsChain
from dlparse.mono.manager import AssetManager
from tests.utils import is_json_schema_match


@pytest.mark.holistic
def test_exported_json(asset_manager: AssetManager):
    entry_dict = export_auto_fs_info_as_entry_dict(asset_manager)

    for entry in entry_dict.values():
        is_json_schema_match(AutoFsChain.json_schema, entry.to_json_entry())
