import pytest

from dlparse.enums import Element, Weapon
from dlparse.export import (export_advanced_info_as_entry_dict)
from dlparse.export.entry import AdvancedInfoEntryBase
from dlparse.mono.manager import AssetManager
from tests.utils import is_json_schema_match

expected_partial_chara_info: dict[int, tuple[Element, str, Weapon, str]] = {
    10150302: (Element.WIND, "エルフィリス（ウエディングVer.）", Weapon.SWD, "早見沙織"),
    10150102: (Element.FLAME, "マルス", Weapon.SWD, "緑川光"),
    10440201: (Element.WATER, "カーリナ", Weapon.AXE, "豊口めぐみ"),
    10350203: (Element.WATER, "チキ", Weapon.DAG, "諸星すみれ"),
}
expected_chara_count_threshold = 252  # As of 2021.05.19-OZuxGHxRaHfdO6li


@pytest.mark.holistic
def test_exported_json(asset_manager: AssetManager):
    entry_dict = export_advanced_info_as_entry_dict(asset_manager)

    for entries in entry_dict.values():
        for entry in entries:
            is_json_schema_match(AdvancedInfoEntryBase.json_schema, entry.to_json_entry())
