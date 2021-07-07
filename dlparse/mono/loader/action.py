"""Classes for managing the action files."""
import os

from dlparse.errors import ActionDataNotFoundError
from dlparse.mono.asset import ActionPartsListAsset, PlayerActionPrefab
from dlparse.utils import is_url

__all__ = ("ActionFileLoader",)


class ActionFileLoader:
    """Class to load the player action files."""

    def _init_path_index(self, asset_parts_list: ActionPartsListAsset, file_root_path: str):
        for parts_entry in asset_parts_list:
            file_path = parts_entry.resource_path_actual

            if is_url(file_root_path):
                path = file_root_path + "/" + file_path
            else:
                path = os.path.join(file_root_path, file_path)

            self._path_index[parts_entry.id] = path

    def __init__(self, asset_parts_list: ActionPartsListAsset, file_root_path: str):
        self._path_index: dict[int, str] = {}  # K = action ID; V = file path
        self._init_path_index(asset_parts_list, file_root_path)

        self._prefab_cache: dict[int, PlayerActionPrefab] = {}

    def get_file_path(self, action_id: int) -> str:
        """
        Get the file path for ``action_id``.

        :raises ActionDataNotFoundError: action file not found
        """
        file_path = self._path_index.get(action_id, None)

        if not file_path:
            raise ActionDataNotFoundError(action_id)

        return file_path

    def get_prefab(self, action_id: int) -> PlayerActionPrefab:
        """
        Get the :class:`PlayerActionPrefab` for ``action_id``.

        The return will be cached for performance improvement.

        :raises ActionDataNotFoundError: action file not found
        """
        file_path = self.get_file_path(action_id)

        if action_id not in self._prefab_cache:
            self._prefab_cache[action_id] = PlayerActionPrefab(action_id, file_path)

        return self._prefab_cache[action_id]

    @staticmethod
    def to_action_file_name(action_id: int) -> str:
        """Get the player action file name of ``action_id``."""
        return f"PlayerAction_{action_id:08}.prefab.json"

    @staticmethod
    def extract_action_id(file_name: str) -> int:
        """
        Extract the action ID from ``file_name``.

        This assumes ``file_name`` is **ALWAYS** in the format of ``PlayerAction_XXXXXXXX.prefab.json``,
        where XXXXXXXX corresponds to the action ID.
        """
        return int(file_name[13:21])
