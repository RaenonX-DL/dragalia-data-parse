"""Base asset class."""
import io
import os
from abc import ABC, abstractmethod
from typing import Any, Generic, Iterator, Optional, TextIO, Type, TypeVar, cast
from urllib.error import HTTPError
from urllib.request import urlopen

from dlparse.enums import Language
from dlparse.errors import ConfigError, LanguageAssetNotFoundError, TextLabelNotFoundError
from dlparse.utils import is_url, localize_asset_path
from .entry import TextEntryBase
from .parser import ParserBase

__all__ = ("AssetBase", "MultilingualAssetBase", "get_file_path", "get_file_like")

THROW_ERROR_ON_FAIL = object()

T = TypeVar("T")
IT = TypeVar("IT")


def get_file_like(file_location: str) -> TextIO:
    """
    Get the file-like object from ``file_location``.

    This currently supports reading file from:

    - Local file path

    - URL
    """
    if is_url(file_location):
        try:
            # `is_url()` already validate ``file_location`` to start with ``http``,
            # no risk of passing ftp:// or file:// here
            # pylint: disable=consider-using-with
            return io.TextIOWrapper(urlopen(file_location), encoding='utf-8')  # nosec
        except HTTPError as ex:
            if ex.code == 404:
                raise ValueError(f"URL: {file_location} not found") from ex

            raise ex

    # Every usages will use `with` statement in the subsequent operations
    # pylint: disable=consider-using-with
    return open(file_location, encoding="utf-8")


def get_file_path(
        default_file_name: Optional[str], /, file_location: Optional[str] = None, asset_dir: Optional[str] = None,
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


class AssetBase(Generic[T, IT], ABC):
    """Base class for the mono behavior assets."""

    asset_file_name: Optional[str] = None

    def __init__(
            self, parser_cls: Type[ParserBase[T]], file_location: Optional[str] = None, /,
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

    def __len__(self) -> int:
        return len(self._data)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} at {self._file_path}>"

    @abstractmethod
    def __iter__(self) -> Iterator[IT]:
        raise NotImplementedError()

    @property
    def data(self) -> T:
        """Get all data of the asset."""
        return self._data


XT = TypeVar("XT", bound=TextEntryBase)
ParsedTextEntryDict = dict[str, XT]


class MultilingualAssetBase(Generic[XT], ABC):
    """Multilingual text asset base class."""

    # pylint: disable=too-few-public-methods

    def __init__(
            self, parser_cls: Type[ParserBase[ParsedTextEntryDict]], asset_dir: str, file_name: str, /,
            is_custom: bool = False,
    ):
        """
        Initializes a multilingual text asset.

        Files to be loaded should be a json. ``file_name`` must **not** include the extension.
        """
        self._assets: dict[str, ParsedTextEntryDict] = {}

        lang: Language
        for lang in Language:
            file_name_join = f"{file_name}.json" if lang.is_main else f"{file_name}@{lang.locale}.json"
            file_path = get_file_path(file_name_join, asset_dir=asset_dir)

            if not lang.is_main and not is_custom:
                file_path = localize_asset_path(file_path, lang)

            file_like = get_file_like(file_path)

            self._assets[lang.value] = cast(ParserBase[ParsedTextEntryDict], parser_cls).parse_file(file_like)

    def get_text(self, lang_code: str, label: str, on_not_found: Any = THROW_ERROR_ON_FAIL) -> str:
        """
        Get the text labeled as ``label`` in ``lang_code``.

        If ``on_not_found`` is not given, an error will be thrown if the text is not found.
        Otherwise, ``on_not_found`` will be returned.

        :raises LanguageAssetNotFoundError: if the language asset for `lang_code` is not found
        :raises TextLabelNotFoundError: if the `label` in `lang_code` is not found and `on_not_found` indicates to
        throw an error
        """
        if not (lang_asset := self._assets.get(lang_code)):
            raise LanguageAssetNotFoundError(lang_code)

        if not (lang_entry := lang_asset.get(label)):
            if on_not_found is THROW_ERROR_ON_FAIL:
                raise TextLabelNotFoundError(label)

            return on_not_found

        return lang_entry.text
