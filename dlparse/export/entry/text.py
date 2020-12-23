"""A text entry containing the text to be used on the website in different languages."""
from dataclasses import InitVar, dataclass, field
from typing import Any, TYPE_CHECKING, Union

from dlparse.enums import Language
from dlparse.errors import MissingTextError, TextLabelNotFoundError
from .base import JsonExportableEntryBase

if TYPE_CHECKING:
    from dlparse.mono.asset.base import MultilingualAssetBase

__all__ = ("TextEntry",)


@dataclass
class TextEntry(JsonExportableEntryBase):
    """A text entry class containing the texts to be displayed on the website in different languages."""

    asset_multilingual: InitVar["MultilingualAssetBase"]

    labels: InitVar[Union[str, list[str]]]
    """List of label to be checked. Only throws error if all the ``labels`` do not have the corresponding text."""

    text_dict: dict[str, str] = field(init=False)

    def __post_init__(self, asset_multilingual: "MultilingualAssetBase", labels: Union[str, list[str]]):
        if isinstance(labels, str):
            labels = [labels]

        self.text_dict = {}
        for lang_code in Language.get_all_available_codes():
            # Check through each label and add the first label which has the text affiliated
            for label in labels:
                try:
                    self.text_dict[lang_code] = asset_multilingual.get_text(lang_code, label)
                    break  # Name found, early terminate the loop
                except TextLabelNotFoundError:
                    continue  # Label not found, try to use the next label

            # Check if the text has been recorded
            if lang_code not in self.text_dict:
                raise MissingTextError(labels, lang_code)

    def to_json_entry(self) -> dict[str, Any]:
        return self.text_dict
