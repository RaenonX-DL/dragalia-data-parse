"""A text entry containing the text to be used on the website in different languages."""
from dataclasses import InitVar, dataclass, field
from typing import Any, Optional, TypeVar, Union

from dlparse.enums import Language
from dlparse.errors import MissingTextError
from dlparse.mono.asset import MultilingualAssetBase, TextAssetMultilingual
from .base import JsonExportableEntryBase

__all__ = ("TextEntry",)

T = TypeVar("T", bound=MultilingualAssetBase)


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

    text_dict: dict[str, str] = field(init=False)

    def __post_init__(self, asset_text_website: T, labels: Union[str, list[str]]):
        if isinstance(labels, str):
            labels = [labels]

        self.text_dict = {}

        for lang_code in Language.get_all_available_codes():
            # Check through each label and add the first label which has the text affiliated
            for label in labels:
                text = asset_text_website.get_text(lang_code, label, on_not_found=None)
                if text is not None:  # Explicit `None` check because empty string is also falsy
                    self.text_dict[lang_code] = text
                    break  # Name found, early terminate the loop

                if not self.asset_text_multi:
                    continue  # Text asset not provided, continue to try the next lang code

                text = self.asset_text_multi.get_text(lang_code, label, on_not_found=None)
                if text is not None:  # Explicit `None` check because empty string is also falsy
                    self.text_dict[lang_code] = text
                    break  # Name found, early terminate the loop

            # Check if the text has been recorded
            if lang_code not in self.text_dict:
                raise MissingTextError(
                    labels, lang_code, f"Text asset{' ' if self.asset_text_multi else ' not '}provided"
                )

    def to_json_entry(self) -> dict[str, Any]:
        return self.text_dict
