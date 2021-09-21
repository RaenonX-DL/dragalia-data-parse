"""A text entry containing the text to be used on the website in different languages."""
from dataclasses import InitVar, dataclass, field
from typing import Any, Optional, TypeVar, Union

from dlparse.enums import Language
from dlparse.errors import MissingTextError
from dlparse.mono.asset import MultilingualAssetBase, TextAssetMultilingual
from .entry import JsonExportableEntryBase
from .type import JsonSchema

__all__ = ("TextEntry",)

T = TypeVar("T", bound=MultilingualAssetBase)

THROW_ERROR = object()


@dataclass
class TextEntry(JsonExportableEntryBase):
    """A text entry class containing the texts to be displayed on the website in different languages."""

    asset_text_website: InitVar[T]
    """Website text asset. The name of this is identical to the one in :class:`AssetManager` for convenience."""

    labels: InitVar[Union[str, list[str]]]
    """List of label to be checked. Only throws error if all the ``labels`` do not have the corresponding text."""

    asset_text_multi: Optional[TextAssetMultilingual] = None
    """
    Official text asset in multi languages.
    The name of this is identical to the one in :class:`AssetManager` for convenience.
    """

    on_not_found: Optional[Any] = THROW_ERROR
    replacements: Optional[dict[str, str]] = None  # K = old string, V = new string
    replacement_ids: Optional[dict[str, str]] = None  # K = old string, V = text label ID

    text_dict: dict[str, str] = field(init=False)

    def _init_get_text_of_label(self, asset_text_website: T, lang_code: Language, labels: Union[str, list[str]]):
        if isinstance(labels, str):
            labels = [labels]

        for label in labels:
            text = asset_text_website.get_text(lang_code, label, on_not_found=None)
            if text is not None:  # Explicit `None` check because empty string is also falsy
                return text

            if not self.asset_text_multi:
                continue  # Text asset not provided, continue to try the next lang code

            text = self.asset_text_multi.get_text(lang_code, label, on_not_found=None)
            if text is not None:  # Explicit `None` check because empty string is also falsy
                return text

        if self.on_not_found is THROW_ERROR:
            raise MissingTextError(
                labels, lang_code, f"Text asset{' ' if self.asset_text_multi else ' not '}provided"
            )

        return self.on_not_found

    def _init_text_dict_fill_content(self, asset_text_website: T, labels: Union[str, list[str]]):
        for lang_code in Language.get_all_available_codes():
            self.text_dict[lang_code] = self._init_get_text_of_label(asset_text_website, lang_code, labels)

    def _init_text_dict_replace_newlines(self):
        self.text_dict = {lang: text.replace("\\n", "\n") for lang, text in self.text_dict.items()}

    def _init_text_dict_replacements(self, asset_text_website: T):
        if not self.replacement_ids:
            return

        new_dict = {}
        for lang, text in self.text_dict.items():
            for old, label in self.replacement_ids.items():
                text = text.replace(old, self._init_get_text_of_label(asset_text_website, Language(lang), label))

            for old, new in self.replacements.items():
                text = text.replace(old, new)

            new_dict[lang] = text

        self.text_dict = new_dict

    def __post_init__(self, asset_text_website: T, labels: Union[str, list[str]]):
        if isinstance(labels, str):
            labels = [labels]

        self.text_dict = {}
        self._init_text_dict_fill_content(asset_text_website, labels)
        self._init_text_dict_replace_newlines()
        self._init_text_dict_replacements(asset_text_website)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {lang: str for lang in Language.get_all_available_codes()}

    def to_json_entry(self) -> dict[str, Any]:
        return self.text_dict
