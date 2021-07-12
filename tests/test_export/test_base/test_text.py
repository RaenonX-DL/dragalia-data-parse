import pytest

from dlparse.errors import MissingTextError
from dlparse.export.entry import TextEntry
from dlparse.mono.manager import AssetManager


def test_replaces_newline(asset_manager: AssetManager):
    entry = TextEntry(
        asset_text_multi=asset_manager.asset_text_multi,
        asset_text_website=asset_manager.asset_text_website,
        labels="SKILL_DETAIL_LV3_108301012"
    )
    assert entry.to_json_entry()["en"] == "Deals flame damage to surrounding enemies,\nand inflicts burn."


def test_error_on_label_missing(asset_manager: AssetManager):
    with pytest.raises(MissingTextError):
        TextEntry(
            asset_text_multi=asset_manager.asset_text_multi,
            asset_text_website=asset_manager.asset_text_website,
            labels="SKILL_DETAIL_LV3_10830101288"
        )


def test_use_on_not_found_text(asset_manager: AssetManager):
    entry = TextEntry(
        asset_text_multi=asset_manager.asset_text_multi,
        asset_text_website=asset_manager.asset_text_website,
        labels="SKILL_DETAIL_LV3_10830101288",
        on_not_found="X"
    )
    assert entry.to_json_entry()["en"] == "X"
