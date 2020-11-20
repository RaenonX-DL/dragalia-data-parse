"""Base asset class."""
import os
from abc import ABC, abstractmethod
from typing import Type, Optional

from .parser import ParserBase

__all__ = ("AssetBase",)


class AssetBase(ABC):
    """Base class for the mono behavior assets."""

    asset_file_name: Optional[str] = None

    def __init__(self, parser_cls: Type[ParserBase], file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        file_path = file_path or (asset_dir and os.path.join(asset_dir, self.asset_file_name))

        if not file_path:
            raise ValueError("Either `file_path` or "
                             "`asset_dir` and `asset_file_name` (class attribute) must be given.")

        self._data = parser_cls.parse_file(file_path)

    def __len__(self):
        return len(self._data)

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()
