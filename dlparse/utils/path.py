"""Util functions for processing the paths."""
import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from dlparse.errors import PathUnlocalizableError
from .string import is_url

if TYPE_CHECKING:
    from dlparse.enums import Language

__all__ = ("localize_asset_path", "localize_path", "make_path")


def localize_asset_path(master_path: str, lang: "Language") -> str:
    """
    Convert ``master_path`` to its corresponding localized path.

    This automatically determines if the path is a network path.

    This WON'T check if ``master_path`` is a master or localized path.
    """
    if lang.is_main:
        return master_path

    is_network_path = is_url(master_path)

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


def localize_path(base_path: str, lang: "Language", /, sub_path: Optional[str] = None) -> str:
    """
    Localize ``base_path`` for ``lang``. The return will be ``<base_path>/localized/<lang>/<sub_path>``.

    Note that for this to handle ``base_path`` as a file, the file name must contain a dot ``.``.
    """
    base_name = os.path.basename(base_path)
    if "." not in base_name:
        # Base path is a directory
        ret = os.path.join(base_path, "localized", lang)
        if sub_path:
            ret = os.path.join(ret, sub_path)

        # Add back trailing slash if it had one
        if base_path.endswith(os.sep):
            ret += os.sep

        return ret

    # Base path is a file
    path = Path(base_path)

    return os.path.join(
        str(path.parent),
        "localized",
        lang,
        os.path.join(sub_path, path.name) if sub_path else path.name
    )


def make_path(*parts: str, is_net: bool) -> str:
    """Make a path from ``parts``. The path format is based on ``is_net``."""
    # Ensure path parts do not have joined parts inside
    parts_processed = []
    for part in parts:
        parts_processed.extend(part.replace("\\", "/").split("/"))

    # Join the path parts back
    if is_net:
        return "/".join(parts_processed)

    # `pylint` false-negative on `os.path.join`, no parameter for `a`
    return os.path.normpath(os.path.join(*parts_processed))  # pylint: disable=no-value-for-parameter
