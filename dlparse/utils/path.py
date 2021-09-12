"""Util functions for processing the paths."""
import os
from typing import TYPE_CHECKING

from dlparse.errors import PathUnlocalizableError

if TYPE_CHECKING:
    from dlparse.enums import Language

__all__ = ("localize_asset_path",)


def localize_asset_path(master_path: str, lang: "Language", is_network_path: bool = False) -> str:
    """
    Convert ``master_path`` to its corresponding localized path.

    This WON'T check if ``master_path`` is a master or localized path.
    """
    if lang.is_main:
        return master_path

    path_parts: list[str]
    if is_network_path:
        path_parts = master_path.split("/")
    else:
        path_parts = os.path.normpath(master_path).split(os.path.sep)

    if "assets" not in path_parts:
        raise PathUnlocalizableError(master_path, lang)

    asset_index = path_parts.index("assets")

    merged_parts = path_parts[:asset_index] + ["localized", lang.locale] + path_parts[asset_index:]

    if is_network_path:
        return "/".join(merged_parts)

    return os.path.join(*merged_parts)
