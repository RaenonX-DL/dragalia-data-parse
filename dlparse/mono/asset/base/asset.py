"""Base asset class."""
import io
import os
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TextIO, Type, TypeVar, Union
from urllib.error import HTTPError
from urllib.request import urlopen

from dlparse.errors import ConfigError, LanguageAssetNotFoundError, TextLabelNotFoundError
from dlparse.utils import is_url
from .entry import TextEntryBase
from .parser import ParserBase

__all__ = ("AssetBase", "MultilingualAssetBase", "get_file_path", "get_file_like")

THROW_ERROR_ON_FAIL = object()


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


def get_file_path(
        default_file_name: str, /, file_location: Optional[str] = None, asset_dir: Optional[str] = None,
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

    if asset_dir and default_file_name:
        if is_url(asset_dir):
            return f"{asset_dir}/{default_file_name}"

        return os.path.join(asset_dir, default_file_name)

    if on_fail is not THROW_ERROR_ON_FAIL:
        return on_fail

    raise ConfigError(
        "Either `file_location` or `asset_dir` and `asset_file_name` (class attribute) must be given."
    )


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
            self._file_path = get_file_path(self.asset_file_name, file_location=file_location, asset_dir=asset_dir)
            file_like = get_file_like(self._file_path)
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


T = TypeVar("T", bound=TextEntryBase)


class MultilingualAssetBase(Generic[T], ABC):
    """Multilingual text asset base class."""

    # pylint: disable=too-few-public-methods

    def __init__(
            self, parser_cls: Type[ParserBase], lang_codes: Union[list[str], dict[str, str]],
            asset_dir: str, file_name: str
    ):
        """
        Initializes a multilingual text asset.

        Files to be loaded should be a json. ``file_name`` must **not** include the extension.

        If ``lang_codes`` is a dict, its key will be the language code for loading the asset,
        and the value is the language code to use for getting the entry.

        An empty ``lang_code`` means to use the default file.
        """
        self._assets: dict[str, dict[str, T]] = {}

        if isinstance(lang_codes, list):
            # Force lang codes to be a `dict`. If it's a list, cast it to a dict
            lang_codes = {lang_code: lang_code for lang_code in lang_codes}

        for lang_code_file, lang_code_asset in lang_codes.items():
            file_name_join = f"{file_name}@{lang_code_file}.json" if lang_code_file else f"{file_name}.json"
            file_path = get_file_path(file_name_join, asset_dir=asset_dir)
            file_like = get_file_like(file_path)

            self._assets[lang_code_asset] = parser_cls.parse_file(file_like)

    def get_text(self, lang_code: str, label: str) -> str:
        """
        Get the text labeled as ``label`` in ``lang_code``.

        :raises LanguageAssetNotFoundError: if the language asset for `lang_code` is not found
        :raises TextLabelNotFoundError: if the `label` in `lang_code` is not found
        """
        # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
        if not (lang_asset := self._assets.get(lang_code)):  # pylint: disable=superfluous-parens
            raise LanguageAssetNotFoundError(lang_code)

        # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
        if not (lang_entry := lang_asset.get(label)):  # pylint: disable=superfluous-parens
            raise TextLabelNotFoundError(label)

        return lang_entry.text
