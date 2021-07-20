import pytest

from dlparse.enums import Element, Language, Weapon
from dlparse.export import export_advanced_info_as_entry_dict
from dlparse.export.entry import AdvancedInfoEntryBase, CharaAdvancedData
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


def test_ability_placeholder_replacements(asset_manager: AssetManager):
    # Summer Celliera
    # https://dragalialost.wiki/w/Summer_Celliera
    data = CharaAdvancedData(asset_manager, [], asset_manager.asset_chara_data.get_data_by_id(10150202))

    ability_2 = data.ability.passive[1].description.text_dict[Language.EN.value]
    assert ability_2 == "Reduces susceptibility to burning by 100%.\n" \
                        "When the user is hit by an attack that would have\n" \
                        "inflicted burning on them, their strength is increased\n" \
                        "by 15% for 10 seconds. After activating, this buff will\n" \
                        "not activate again for 15 seconds."

    ex_ability = data.ability.co_ability.global_.description.text_dict[Language.EN.value]
    assert ex_ability == "Increases dragon gauge fill rate by 15%.\nBenefits your whole team."

    cex_ability = data.ability.co_ability.chained.description.text_dict[Language.EN.value]
    assert cex_ability == "If a team member is attuned to Water:\n" \
                          "each shapeshift increases their strength\n" \
                          "(up to three times per quest).\n" \
                          "Benefits your whole team."
