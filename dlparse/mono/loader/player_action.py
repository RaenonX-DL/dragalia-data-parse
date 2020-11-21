"""Classes for getting the player action file path."""
import os

from dlparse.mono.asset import PlayerActionPrefab

__all__ = ("PlayerActionFileLoader",)


class PlayerActionFileLoader:
    """Class to load the player action files."""

    def _init_path_index(self, file_root_path: str):
        for path, _, files in os.walk(file_root_path):
            for name in files:
                action_id = self.extract_action_id(name)

                self._path_index[action_id] = os.path.join(path, name)

    def __init__(self, file_root_path: str):
        self._path_index: dict[int, str] = {}  # K = action ID; V = file path
        self._init_path_index(file_root_path)

        self._prefab_cache: dict[int, PlayerActionPrefab] = {}

    def get_file_path(self, action_id: int) -> str:
        """
        Get the file path for ``action_id``.

        :raises FileNotFoundError: action file not found
        """
        file_path = self._path_index.get(action_id, None)

        if not file_path:
            raise FileNotFoundError(f"File for action ID {action_id} not found")

        return file_path

    def get_prefab(self, action_id: int) -> PlayerActionPrefab:
        """
        Get the :class:`PlayerActionPrefab` for ``action_id``.

        The return will be cached for performance improvement.

        :raises FileNotFoundError: action file not found
        """
        file_path = self.get_file_path(action_id)

        if action_id not in self._prefab_cache:
            self._prefab_cache[action_id] = PlayerActionPrefab(file_path)

        return self._prefab_cache[action_id]

    @staticmethod
    def extract_action_id(file_name: str) -> int:
        """
        Extract the action ID from ``file_name``.

        This assumes ``file_name`` is **ALWAYS** in the format of ``PlayerAction_XXXXXXXX.prefab.json``,
        where XXXXXXXX corresponds to the action ID.
        """
        return int(file_name[13:21])
