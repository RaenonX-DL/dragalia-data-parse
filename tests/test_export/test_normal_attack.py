import pytest

from dlparse.export import export_normal_attack_info_as_entry_dict
from dlparse.export.entry import NormalAttackChainEntry
from dlparse.mono.manager import AssetManager
from tests.utils import is_json_schema_match


@pytest.mark.holistic
def test_exported_json(asset_manager: AssetManager):
    entry_dict = export_normal_attack_info_as_entry_dict(asset_manager)

    for entries in entry_dict.values():
        for entry in entries:
            is_json_schema_match(NormalAttackChainEntry.json_schema, entry.to_json_entry())
