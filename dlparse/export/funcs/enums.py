"""Functions to export the enums."""
from enum import Enum
from typing import Sequence, TYPE_CHECKING, Type, TypeVar

from dlparse.enums import get_image_path
from dlparse.export.entry import EnumEntry, TextEntry
from .base import export_as_json

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("export_enums_entries", "export_enums_json")

T = TypeVar("T", bound=Enum)
ET = TypeVar("ET", bound=EnumEntry)


def export_enums_entries(
        asset_manager: "AssetManager", enums_to_export: dict[str, Sequence[T]], /,
        prefix: str = "ENUM_", enum_entry_class: Type[ET] = EnumEntry
) -> dict[str, list[ET]]:
    """
    Export ``enums_to_export`` as a list of :class:`EnumEntry` to be exported to a file.

    The key of ``enums_to_export`` is the name of the enums, which will be the key(s) in the exported json.
    """
    ret: dict[str, list[enum_entry_class]] = {}

    for enum_name, enum_list in enums_to_export.items():
        if enum_name not in ret:
            ret[enum_name] = []

        for enum in enum_list:
            ret[enum_name].append(enum_entry_class(
                enum_name=enum.name, enum_code=enum.value, enum_image_path=get_image_path(enum),
                trans=TextEntry(asset_manager.asset_text_website, f"{prefix}{enum.name}")
            ))

    return ret


def export_enums_json(
        asset_manager: "AssetManager", enums_to_export: dict[str, Sequence[T]], file_path: str, /,
        prefix: str = "ENUM_"
):
    """
    Export ``enums_to_export`` to ``file_path`` as a json file.

    The key of ``enums_to_export`` is the name of the enums, which will be the key(s) in the exported json.
    """
    export_as_json(export_enums_entries(asset_manager, enums_to_export, prefix=prefix), file_path)
