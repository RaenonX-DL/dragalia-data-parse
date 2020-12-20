"""Functions to export the enums."""
from enum import Enum
from typing import Sequence, TYPE_CHECKING, TypeVar

from dlparse.enums import Language
from dlparse.export.entry import EnumEntry
from .base import export_as_json

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("export_enums_entries", "export_enums_json")

T = TypeVar("T", bound=Enum)


def export_enums_entries(
        asset_manager: "AssetManager", enums_to_export: dict[str, Sequence[T]]
) -> dict[str, list[EnumEntry]]:
    """Export ``enums_to_export`` as a list of :class:`EnumEntry` to be exported to a file."""
    ret: dict[str, list[EnumEntry]] = {}

    for enum_name, enum_list in enums_to_export.items():
        if enum_name not in ret:
            ret[enum_name] = []

        for enum in enum_list:
            # Get all translations for each enum
            trans = {
                lang_code: asset_manager.asset_text_website.get_text(lang_code, f"ENUM_{enum.name}")
                for lang_code in Language.get_all_available_codes()
            }

            ret[enum_name].append(EnumEntry(
                enum_name=enum.name, enum_code=enum.value,
                trans=trans
            ))

    return ret


def export_enums_json(asset_manager: "AssetManager", enums_to_export: dict[str, Sequence[T]], file_path: str):
    """Export ``enums_to_export`` to ``file_path`` as a json file."""
    export_as_json(export_enums_entries(asset_manager, enums_to_export), file_path)
