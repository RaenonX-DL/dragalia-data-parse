"""Base asset class."""
import os
from abc import ABC, abstractmethod
from typing import Type, Optional

from dlparse.errors import ConfigError
from .parser import ParserBase

__all__ = ("AssetBase",)


class AssetBase(ABC):
    """Base class for the mono behavior assets."""

    asset_file_name: Optional[str] = None

    def __init__(self, parser_cls: Type[ParserBase], file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        file_path = self.get_file_path(file_path=file_path, asset_dir=asset_dir)

        if not file_path:
            raise ConfigError("Either `file_path` or "
                              "`asset_dir` and `asset_file_name` (class attribute) must be given.")

        self._data = parser_cls.parse_file(file_path)

    def __len__(self):
        return len(self._data)

    @classmethod
    def get_file_path(cls, *, file_path: Optional[str] = None, asset_dir: Optional[str] = None):
        """
        Get the file path.

        If ``file_path`` is provided, ``file_path`` will be returned.

        If ``asset_dir`` is provided, ``asset_dir`` will be used as the folder of the asset,
        with a file named ``asset_file_name``.

        If both are provided, ``asset_dir`` will be ignored.

        If nothing is provided, ``None`` will be returned.
        """
        return file_path or (asset_dir and os.path.join(asset_dir, cls.asset_file_name))

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()
