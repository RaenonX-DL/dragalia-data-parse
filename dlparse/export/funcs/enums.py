"""Functions to export the enums."""
from typing import Sequence, TYPE_CHECKING, Type, TypeVar

from dlparse.enums import TranslatableEnumMixin, get_image_path
from dlparse.export.entry import EnumEntry, TextEntry
from .base import export_as_json

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("export_enums_entries", "export_enums_json")

T = TypeVar("T", bound=TranslatableEnumMixin)
ET = TypeVar("ET", bound=EnumEntry)


def export_enums_entries(
        asset_manager: "AssetManager", enums_to_export: dict[str, Sequence[T]], /,
        enum_entry_class: Type[ET] = EnumEntry
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
                name=enum.name, code=enum.value, image_path=get_image_path(enum, on_not_found=None),
                trans=TextEntry(
                    asset_text_base=asset_manager.asset_text_website, labels=enum.translation_id,
                    asset_text_additional=asset_manager.asset_text_multi
                )
            ))

    return ret


def export_enums_json(
        asset_manager: "AssetManager", enums_to_export: dict[str, Sequence[T]], file_path: str
):
    """
    Export ``enums_to_export`` to ``file_path`` as a json file.

    The key of ``enums_to_export`` is the name of the enums, which will be the key(s) in the exported json.
    """
    export_as_json(export_enums_entries(asset_manager, enums_to_export), file_path)
