from typing import Sequence, TypeVar

from dlparse.enums import (
    AbilityTargetAction, Condition, Element, HitTargetSimple, Language, Status, TranslatableEnumMixin,
    cond_afflictions, cond_elements,
)
from dlparse.export import (
    collect_chained_ex_ability_buff_param, collect_ex_ability_buff_param, export_condition_entries,
    export_enums_entries,
)
from dlparse.export.funcs.enum_cond import condition_theme
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer

T = TypeVar("T", bound=TranslatableEnumMixin)


def export_enum(asset_manager: AssetManager, key: str, enums: Sequence[T]):
    entries = export_enums_entries(asset_manager, {key: enums})

    assert len(entries) > 0

    conditions_missing: set[str] = {elem.name for elem in enums}

    for entry in entries[key]:
        conditions_missing.remove(entry.enum_name)

        assert Language.CHT.value in entry.trans.text_dict
        assert Language.EN.value in entry.trans.text_dict
        assert Language.JP.value in entry.trans.text_dict

    assert len(conditions_missing) == 0, f"Missing conditions: {conditions_missing}"


def test_export_affliction_conditions(asset_manager: AssetManager):
    export_enum(asset_manager, "affliction", cond_afflictions)


def test_export_element_conditions(asset_manager: AssetManager):
    export_enum(asset_manager, "elementConditions", cond_elements)


def test_export_element_enums(asset_manager: AssetManager):
    export_enum(asset_manager, "element", Element.get_all_valid_elements())
    export_enum(asset_manager, "element", Element.get_all_translatable_members())


def test_export_status_enums(asset_manager: AssetManager):
    export_enum(asset_manager, "status", Status.get_all_translatable_members())


def test_export_hit_target_enums(asset_manager: AssetManager):
    export_enum(asset_manager, "hitTargetSimple", HitTargetSimple.get_all_translatable_members())


def test_export_ability_target_action_enums(asset_manager: AssetManager):
    export_enum(asset_manager, "abilityTargetAction", AbilityTargetAction.get_all_translatable_members())


def test_export_ex_ability_buff_params(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    export_enum(asset_manager, "exBuffParam", collect_ex_ability_buff_param(transformer_ability, asset_manager))


def test_export_chained_ex_ability_buff_params(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    export_enum(
        asset_manager, "cexBuffParam", collect_chained_ex_ability_buff_param(transformer_ability, asset_manager)
    )


def test_export_condition_enums(asset_manager: AssetManager):
    entries = export_condition_entries(asset_manager)

    assert len(entries) == len(Condition)

    for cond_code, entry in entries.items():
        condition = Condition(cond_code)

        if condition not in condition_theme:
            continue

        assert condition_theme[condition] == entry.color_theme
