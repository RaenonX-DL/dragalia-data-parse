from dlparse.enums import Condition, Element, Language, cond_afflictions, cond_elements
from dlparse.export import (
    collect_chained_ex_ability_buff_param, collect_ex_ability_buff_param, export_condition_entries,
    export_enums_entries,
)
from dlparse.export.funcs.enum_cond import condition_theme
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer


def test_export_affliction_conditions(asset_manager: AssetManager):
    key = "affliction"

    entries = export_enums_entries(asset_manager, {key: cond_afflictions})

    assert len(entries) > 0

    conditions_missing: set[str] = {cond.name for cond in cond_afflictions}

    for entry in entries[key]:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans.text_dict
        assert Language.EN.value in entry.trans.text_dict
        assert Language.JP.value in entry.trans.text_dict

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"


def test_export_elements_conditions(asset_manager: AssetManager):
    key = "element"

    entries = export_enums_entries(asset_manager, {key: cond_elements})

    assert len(entries) > 0

    conditions_missing: set[str] = {cond.name for cond in cond_elements}

    for entry in entries[key]:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans.text_dict
        assert Language.EN.value in entry.trans.text_dict
        assert Language.JP.value in entry.trans.text_dict

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"


def test_export_element_enums(asset_manager: AssetManager):
    key = "element"

    entries = export_enums_entries(asset_manager, {key: Element.get_all_valid_elements()})

    assert len(entries) > 0

    conditions_missing: set[str] = {elem.name for elem in Element.get_all_valid_elements()}

    for entry in entries[key]:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans.text_dict
        assert Language.EN.value in entry.trans.text_dict
        assert Language.JP.value in entry.trans.text_dict

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"


def test_export_ex_ability_buff_params(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    key = "exBuffParam"

    entries = export_enums_entries(
        asset_manager, {key: collect_ex_ability_buff_param(transformer_ability, asset_manager)},
        prefix="ENUM_BUFF_"
    )

    assert len(entries) > 0

    conditions_missing: set[str] = {
        buff_param.name for buff_param in collect_ex_ability_buff_param(transformer_ability, asset_manager)
    }

    for entry in entries[key]:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans.text_dict
        assert Language.EN.value in entry.trans.text_dict
        assert Language.JP.value in entry.trans.text_dict

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"


def test_export_chained_ex_ability_buff_params(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    key = "cexBuffParam"

    entries = export_enums_entries(
        asset_manager, {key: collect_chained_ex_ability_buff_param(transformer_ability, asset_manager)},
        prefix="ENUM_BUFF_"
    )

    assert len(entries) > 0

    conditions_missing: set[str] = {
        buff_param.name for buff_param in collect_chained_ex_ability_buff_param(transformer_ability, asset_manager)
    }

    for entry in entries[key]:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans.text_dict
        assert Language.EN.value in entry.trans.text_dict
        assert Language.JP.value in entry.trans.text_dict

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"


def test_export_condition_enums(asset_manager: AssetManager):
    entries = export_condition_entries(asset_manager)

    assert len(entries) == len(Condition)

    for cond_code, entry in entries.items():
        condition = Condition(cond_code)

        if condition not in condition_theme:
            continue

        assert condition_theme[condition] == entry.color_theme
