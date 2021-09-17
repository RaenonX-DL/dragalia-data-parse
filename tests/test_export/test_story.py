import pytest

from dlparse.enums import Language
from dlparse.export import export_unit_story_as_entry_dict
from dlparse.mono.manager import AssetManager


@pytest.mark.holistic
def test_exported_entries(asset_manager: AssetManager):
    entry_dict = export_unit_story_as_entry_dict(asset_manager, Language.CHT, skip_unparsable=False)

    assert len(entry_dict) > 0
