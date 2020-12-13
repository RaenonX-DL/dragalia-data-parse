"""Base asset class."""
import io
import os
from abc import ABC, abstractmethod
from typing import Any, Optional, TextIO, Type, Union
from urllib.error import HTTPError
from urllib.request import urlopen

from dlparse.errors import ConfigError
from dlparse.utils import is_url
from .parser import ParserBase

__all__ = ("AssetBase",)


THROW_ERROR_ON_FAIL = object()


class AssetBase(ABC):
    """Base class for the mono behavior assets."""

    asset_file_name: Optional[str] = None

    def __init__(
            self, parser_cls: Type[ParserBase], file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        if not file_location and not asset_dir and not file_like:
            raise ConfigError(
                "Either `file_location`, `asset_dir` and `asset_file_name` (class attribute) or `file_like` "
                "must be given to load the asset."
            )

        if not file_like:
            self._file_path = self.get_file_path(file_location=file_location, asset_dir=asset_dir)
            file_like = self.get_file_like(self._file_path)
        else:
            self._file_path = file_like.name

        with file_like:
            self._data = parser_cls.parse_file(file_like)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<{self.__class__.__name__} at {self._file_path}>"

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()

    @property
    def data(self) -> Union[dict, list, set]:
        """Get all data of the asset."""
        return self._data

    @staticmethod
    def get_file_like(file_location: str) -> TextIO:
        """
        Get the file-like object from ``file_location``.

        This currently supports reading file from:

        - Local file path

        - URL
        """
        if is_url(file_location):
            try:
                return io.TextIOWrapper(urlopen(file_location), encoding='utf-8')
            except HTTPError as ex:
                if ex.code == 404:
                    raise ValueError(f"URL: {file_location} not found") from ex

                raise ex

        return open(file_location, encoding="utf-8")

    @classmethod
    def get_file_path(
            cls, /, file_location: Optional[str] = None, asset_dir: Optional[str] = None,
            on_fail: Any = THROW_ERROR_ON_FAIL
    ) -> str:
        """
        Get the complete path of a file with the given parameter.

        If ``file_location`` is provided, ``file_location`` will be returned.

        If ``asset_dir`` is provided and ``asset_file_name`` (class attribute) is set,
        ``asset_dir`` will be used as the folder of the asset with a file named ``asset_file_name`` (class attribute).

        If both are provided, ``asset_dir`` will be ignored.

        If nothing is provided, :class:`ConfigError` is raised if nothing is specified as ``on_fail``.
        Otherwise, return ``on_fail``.

        :raises ConfigError: if the path is failed to get, and nothing has been set to `on_fail`
        """
        if file_location:
            return file_location

        if asset_dir and cls.asset_file_name:
            if is_url(asset_dir):
                return f"{asset_dir}/{cls.asset_file_name}"

            return os.path.join(asset_dir, cls.asset_file_name)

        if on_fail is not THROW_ERROR_ON_FAIL:
            return on_fail

        raise ConfigError(
            "Either `file_location` or `asset_dir` and `asset_file_name` (class attribute) must be given."
        )
