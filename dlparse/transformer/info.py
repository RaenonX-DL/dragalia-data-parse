"""
Various info transformer.

This will not do heavy calculations.
This serves as a middleman that only process the raw data as needed for the use of the website.
"""
from typing import Optional, TYPE_CHECKING

from dlparse.model import CharaInfo, DragonInfo

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("InfoTransformer",)


class InfoTransformer:
    """
    Various info transformer.

    This transforms the items below to be exported:

    - Character data entry
    - Dragon data entry
    """

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_manager: "AssetManager" = asset_manager

    def transform_chara_info(self, chara_id: int) -> Optional[CharaInfo]:
        """Get the info of character data at ``chara_id``."""
        chara_data = self._asset_manager.asset_chara_data.get_data_by_id(chara_id)

        if not chara_data:
            return None

        return CharaInfo(chara_data)

    def transform_dragon_info(self, dragon_id: int) -> Optional[DragonInfo]:
        """Get the info of dragon data at ``dragon_id``."""
        dragon_data = self._asset_manager.asset_dragon_data.get_data_by_id(dragon_id)

        if not dragon_data:
            return None

        return DragonInfo(dragon_data)
