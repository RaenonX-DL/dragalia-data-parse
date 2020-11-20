"""Classes for getting the player action file path."""
import os


__all__ = ("PlayerActionFilePathFinder",)


class PlayerActionFilePathFinder:
    """Class to index the player action file paths for easier access."""

    def _init_indexing(self, file_root_path: str):
        for path, _, files in os.walk(file_root_path):
            for name in files:
                action_id = self.extract_action_id(name)

                self._index[action_id] = os.path.join(path, name)

    def __init__(self, file_root_path: str):
        self._index: dict[int, str] = {}  # K = action ID; V = file path
        self._init_indexing(file_root_path)

    def get_file_path(self, action_id: int) -> str:
        """
        Get the file path for ``action_id``.

        :raises FileNotFoundError: action file not found
        """
        file_path = self._index.get(action_id, None)

        if not file_path:
            raise FileNotFoundError(f"File for action ID {action_id} not found")

        return file_path

    @staticmethod
    def extract_action_id(file_name: str) -> int:
        """
        Extract the action ID from ``file_name``.

        This assumes ``file_name`` is **ALWAYS** in the format of ``PlayerAction_XXXXXXXX.prefab.json``,
        where XXXXXXXX corresponds to the action ID.
        """
        return int(file_name[13:21])
