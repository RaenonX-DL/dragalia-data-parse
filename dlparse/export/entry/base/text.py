"""A text entry containing the text to be used on the website in different languages."""
from dataclasses import InitVar, dataclass, field
from typing import Any, Optional, Union

from dlparse.enums import Language
from dlparse.errors import MissingTextError
from dlparse.mono.asset import MultilingualAssetBase
from .entry import JsonExportableEntryBase
from .type import JsonSchema

__all__ = ("TextEntry",)

THROW_ERROR = object()


@dataclass
class TextEntry(JsonExportableEntryBase):
    """A text entry class containing the texts to be displayed on the website in different languages."""

    asset_text_base: InitVar[MultilingualAssetBase]
    """Base text asset to use for getting the actual text."""

    labels: InitVar[Union[str, list[str]]]
    """List of label to be checked. Only throws error if all the ``labels`` do not have the corresponding text."""

    include_partial_support: InitVar[bool] = False

    asset_text_additional: Optional[MultilingualAssetBase] = None
    """Additional text asset to use if the given text label is not found in ``asset_text_base``."""

    on_not_found: Optional[Any] = THROW_ERROR
    replacements: Optional[dict[str, str]] = None  # K = old string, V = new string
    replacement_ids: Optional[dict[str, str]] = None  # K = old string, V = text label ID

    text_dict: dict[str, str] = field(init=False)

    def _init_get_text_of_label(
            self, asset_text_base: MultilingualAssetBase, lang: Language, labels: Union[str, list[str]]
    ):
        lang_code = lang.value

        if isinstance(labels, str):
            labels = [labels]

        for label in labels:
            text = asset_text_base.get_text(lang_code, label, on_not_found=None)
            if text is not None:  # Explicit `None` check because empty string is also falsy
                return text

            if not self.asset_text_additional:
                continue  # Text asset not provided, continue to try the next lang code

            text = self.asset_text_additional.get_text(lang_code, label, on_not_found=None)
            if text is not None:  # Explicit `None` check because empty string is also falsy
                return text

        if self.on_not_found is THROW_ERROR:
            raise MissingTextError(
                labels, lang_code, f"Text asset{' ' if self.asset_text_additional else ' not '}provided"
            )

        return self.on_not_found

    def _init_text_dict_fill_content(
            self, asset_text_base: MultilingualAssetBase, labels: Union[str, list[str]], include_partial_support: bool
    ):
        for lang in Language:
            lang: Language
            if not include_partial_support and not lang.is_fully_supported:
                continue

            self.text_dict[lang.value] = self._init_get_text_of_label(asset_text_base, lang, labels)

    def _init_text_dict_replace_newlines(self):
        self.text_dict = {lang: text.replace("\\n", "\n") for lang, text in self.text_dict.items()}

    def _init_text_dict_replacements(self, asset_text_base: MultilingualAssetBase):
        if not self.replacement_ids:
            return

        new_dict = {}
        for lang, text in self.text_dict.items():
            for old, label in self.replacement_ids.items():
                text = text.replace(old, self._init_get_text_of_label(asset_text_base, Language(lang), label))

            for old, new in self.replacements.items():
                text = text.replace(old, new)

            new_dict[lang] = text

        self.text_dict = new_dict

    def __post_init__(
            self, asset_text_base: MultilingualAssetBase, labels: Union[str, list[str]], include_partial_support: bool
    ):
        if isinstance(labels, str):
            labels = [labels]

        self.text_dict = {}
        self._init_text_dict_fill_content(asset_text_base, labels, include_partial_support)
        self._init_text_dict_replace_newlines()
        self._init_text_dict_replacements(asset_text_base)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {lang: str for lang in Language.get_all_available_codes()}

    def to_json_entry(self) -> dict[str, Any]:
        return self.text_dict
