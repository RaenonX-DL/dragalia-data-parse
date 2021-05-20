import pytest

from dlparse.enums import Element, Language, Weapon
from dlparse.export import export_chara_info_as_entries, export_dragon_info_as_entries
from dlparse.mono.manager import AssetManager

expected_partial_chara_info: dict[int, tuple[Element, str, Weapon, str]] = {
    10150302: (Element.WIND, "エルフィリス（ウエディングVer.）", Weapon.SWD, "早見沙織"),
    10150102: (Element.FLAME, "マルス", Weapon.SWD, "緑川光"),
    10440201: (Element.WATER, "カーリナ", Weapon.AXE, "豊口めぐみ"),
    10350203: (Element.WATER, "チキ", Weapon.DAG, "諸星すみれ"),
}
expected_chara_count_threshold = 252  # As of 2021.05.19-OZuxGHxRaHfdO6li


@pytest.mark.holistic
def test_exported_chara_entries(asset_manager: AssetManager):
    entries = export_chara_info_as_entries(asset_manager, skip_unparsable=False)

    assert len(entries) >= expected_chara_count_threshold

    chara_ids_missing: set[int] = set(expected_partial_chara_info.keys())

    for entry in entries:
        actual_info = (
            entry.unit_element,
            entry.unit_name.text_dict[Language.JP],
            entry.weapon,
            entry.unit_cv_jp.text_dict[Language.JP],
        )

        if entry.unit_id in chara_ids_missing:
            chara_ids_missing.remove(entry.unit_id)

        if expected_info := expected_partial_chara_info.get(entry.unit_id):
            assert expected_info == actual_info, f"Chara info mismatch: {entry.unit_id}"

    assert len(chara_ids_missing) == 0, f"Chara IDs missing: {chara_ids_missing}"


@pytest.mark.holistic
def test_exported_chara_json(asset_manager: AssetManager):
    # FIXME: Utils for schema matching - this is too hard to read
    entries = export_chara_info_as_entries(asset_manager)

    for entry in entries:
        json_entry = entry.to_json_entry()

        # Check for unit keys
        for chara_key in ("name", "iconName", "id", "element", "rarity", "releaseEpoch",):
            assert chara_key in json_entry

        # Check for chara keys
        for chara_key in ("weapon", "hasUniqueDragon"):
            assert chara_key in json_entry

        # Check for the keys in the names
        for lang_key in ("cht", "en", "jp"):
            assert lang_key in json_entry["cvEn"]
            assert lang_key in json_entry["cvJp"]


expected_partial_dragon_info: dict[int, tuple[Element, int, str, str]] = {
    20050113: (Element.FLAME, 5, "マーズ（ドラフェスVer.）", ""),
    20050414: (Element.LIGHT, 5, "ジャンヌブレイヴ（ドラフェスVer.）", "潘めぐみ"),
    20050107: (Element.FLAME, 5, "コノハナサクヤ", "中原麻衣"),
    20040101: (Element.FLAME, 4, "ブリュンヒルデ", "遠藤綾"),
}


@pytest.mark.holistic
def test_exported_dragon_entries(asset_manager: AssetManager):
    entries = export_dragon_info_as_entries(asset_manager, skip_unparsable=False)

    assert len(entries) > 0

    dragon_ids_missing: set[int] = set(expected_partial_dragon_info.keys())

    for entry in entries:
        actual_info = (
            entry.unit_element,
            entry.unit_rarity,
            entry.unit_name.text_dict[Language.JP],
            entry.unit_cv_jp.text_dict[Language.JP],
        )

        if entry.unit_id in dragon_ids_missing:
            dragon_ids_missing.remove(entry.unit_id)

        if expected_info := expected_partial_dragon_info.get(entry.unit_id):
            assert expected_info == actual_info, f"Dragon info mismatch: {entry.unit_id}"

    assert len(dragon_ids_missing) == 0, f"Dragon IDs missing: {dragon_ids_missing}"


@pytest.mark.holistic
def test_exported_dragon_json(asset_manager: AssetManager):
    entries = export_dragon_info_as_entries(asset_manager)

    for entry in entries:
        json_entry = entry.to_json_entry()

        # Check for unit keys
        for chara_key in ("name", "iconName", "id", "element", "rarity", "releaseEpoch",):
            assert chara_key in json_entry

        # Check for the keys in the names
        for lang_key in ("cht", "en", "jp"):
            assert lang_key in json_entry["cvEn"]
            assert lang_key in json_entry["cvJp"]
