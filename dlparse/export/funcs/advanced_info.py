"""Functions to export advanced unit info, including characters and dragons."""
import os
from typing import Type, TypeVar, Union

from dlparse.export.entry import AdvancedInfoEntryBase, CharaAdvancedData, DragonAdvancedData
from dlparse.mono.asset import CharaDataEntry, DragonDataEntry, UnitEntry
from dlparse.mono.manager import AssetManager
from .base import export_as_json, export_each_chara_entries, export_each_dragon_entries
from .skill_atk import export_atk_skills

__all__ = ("export_advanced_info_as_entry_dict", "export_advanced_info_as_json")

TB = TypeVar("TB", bound=AdvancedInfoEntryBase)
TU = TypeVar("TU", bound=UnitEntry)


def export_advanced_info(
        unit_entry: TU, asset_manager: AssetManager, advanced_data_class: Type[TB], /,
        skip_unparsable: bool = True
) -> tuple[list[TB], list[str]]:
    """
    Parse ``unit_entry`` to an advanced unit info entry.

    Note that the returned entry array always contain a single element only.
    """
    atk_skills, skipped_messages = export_atk_skills(unit_entry, asset_manager, skip_unparsable=skip_unparsable)

    if skipped_messages:
        return [], skipped_messages

    return [advanced_data_class(asset_manager, atk_skills, unit_entry)], []


def export_advanced_info_chara(
        chara_entry: CharaDataEntry, asset_manager: AssetManager, skip_unparsable: bool = True
) -> tuple[list[CharaAdvancedData], list[str]]:
    """
    Transform ``chara_entry`` to an exportable advanced info entry.

    Note that the returned entry array always contain a single element only.
    """
    return export_advanced_info(chara_entry, asset_manager, CharaAdvancedData, skip_unparsable=skip_unparsable)


def export_advanced_info_dragon(
        dragon_entry: DragonDataEntry, asset_manager: AssetManager, skip_unparsable: bool = True
) -> tuple[list[DragonAdvancedData], list[str]]:
    """
    Transform ``dragon_entry`` to an exportable advanced info entry.

    Note that the returned entry array always contain a single element only.
    """
    return export_advanced_info(dragon_entry, asset_manager, DragonAdvancedData, skip_unparsable=skip_unparsable)


def export_advanced_info_as_entry_dict(
        asset_manager: AssetManager, /, skip_unparsable: bool = True
) -> dict[int, list[Union[CharaAdvancedData, DragonAdvancedData]]]:
    """
    Export the advanced info of all units (characters, dragons) as an entry dict.

    The key of the return is the unit ID;
    The value of the return is the corresponding info entry.

    Note that the value of the return always contain a single element.
    """
    ret = {}
    # Export character advanced info
    ret.update(export_each_chara_entries(
        export_advanced_info_chara, asset_manager,
        skip_unparsable=skip_unparsable,
    ))
    # Export dragon normal attack info
    ret.update(export_each_dragon_entries(
        export_advanced_info_dragon, asset_manager,
        skip_unparsable=skip_unparsable
    ))
    return ret


def export_advanced_info_as_json(file_dir: str, asset_manager: AssetManager, /, skip_unparsable: bool = True):
    """Export all advanced unit info as json."""
    entries = export_advanced_info_as_entry_dict(asset_manager, skip_unparsable=skip_unparsable)

    for unit_id, info_entry in entries.items():
        export_as_json(info_entry[0].to_json_entry(), os.path.join(file_dir, f"{unit_id}.json"))
