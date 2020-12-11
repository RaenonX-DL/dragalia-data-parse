"""Classes for handling the action parts list asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("ActionPartsListEntry", "ActionPartsListAsset", "ActionPartsListParser")


@dataclass
class ActionPartsListEntry(MasterEntryBase):
    """Single action parts list entry."""

    resource_path: str
    resource_path_actual: str

    @staticmethod
    def get_actual_path(resource_path: str) -> str:
        """Get the actual relative path (parts list asset as root) of an action part."""
        # Take out the prefixed `Actions/`
        actual_path = resource_path[8:]

        # Only lower the case before the right-most slash ("/") - this is the case our data depot is using
        rslash_idx = actual_path.rindex("/")
        actual_path = actual_path[:rslash_idx].lower() + actual_path[rslash_idx:]

        # Then append `.prefab.json` to the path
        actual_path += ".prefab.json"

        return actual_path

    @staticmethod
    def get_action_id(resource_path: str) -> int:
        """Get the action ID from ``resource_path``."""
        # Take the last 8 chars to be action ID
        return int(resource_path[-8:])

    @staticmethod
    def parse_raw(data: dict[str, Union[str, str]]) -> "ActionPartsListEntry":
        # Resource path is expected to be in the format of `Actions/CommonAction/cmn/CommonAction_00000001`
        resource_path = data["_resourcePath"]

        action_id = ActionPartsListEntry.get_action_id(resource_path)
        actual_path = ActionPartsListEntry.get_actual_path(resource_path)

        return ActionPartsListEntry(
            id=action_id,
            resource_path=resource_path,
            resource_path_actual=actual_path
        )


class ActionPartsListAsset(MasterAssetBase[ActionPartsListEntry]):
    """Action parts list asset class."""

    asset_file_name = "ActionPartsList.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(ActionPartsListParser, file_location, asset_dir=asset_dir, file_like=file_like)


class ActionPartsListParser(MasterParserBase[ActionPartsListEntry]):
    """Class to parse the action parts list file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, ActionPartsListEntry]:
        entries = cls.get_entries_list(file_like)

        ret: dict[int, ActionPartsListEntry] = {}

        for value in entries:
            entry = ActionPartsListEntry.parse_raw(value)
            ret[entry.id] = entry

        return ret
