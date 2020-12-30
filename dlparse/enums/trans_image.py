"""Implementations of getting the related image of an enum."""
from typing import Dict, Optional, Union

from .condition import Condition
from .element import Element

__all__ = ("get_image_path",)

TransformableEnums = Union[Condition, Element]

path_dict: Dict[TransformableEnums, str] = {
    Element.FLAME: "/icon/element/m/Icon_02_Flame.png",
    Element.WATER: "/icon/element/m/Icon_02_Water.png",
    Element.WIND: "/icon/element/m/Icon_02_Wind.png",
    Element.LIGHT: "/icon/element/m/Icon_02_Light.png",
    Element.SHADOW: "/icon/element/m/Icon_02_Dark.png",
    Condition.TARGET_POISONED: "/icon/status/Icon_Status_01_01.png",
    Condition.TARGET_BURNED: "/icon/status/Icon_Status_01_02.png",
    Condition.TARGET_FROZEN: "/icon/status/Icon_Status_01_03.png",
    Condition.TARGET_PARALYZED: "/icon/status/Icon_Status_01_04.png",
    Condition.TARGET_BLINDED: "/icon/status/Icon_Status_01_05.png",
    Condition.TARGET_STUNNED: "/icon/status/Icon_Status_01_06.png",
    Condition.TARGET_CURSED: "/icon/status/Icon_Status_01_07.png",
    Condition.TARGET_BOGGED: "/icon/status/Icon_Status_01_09.png",
    Condition.TARGET_SLEPT: "/icon/status/Icon_Status_01_10.png",
    Condition.TARGET_FROSTBITTEN: "/icon/status/Icon_Status_01_11.png",
    Condition.TARGET_FLASHBURNED: "/icon/status/Icon_Status_01_12.png",
    Condition.TARGET_STORMLASHED: "/icon/status/Icon_Status_01_13.png",
    Condition.TARGET_SHADOWBLIGHTED: "/icon/status/Icon_Status_01_14.png",
    Condition.TARGET_SCORCHRENT: "/icon/status/Icon_Status_01_15.png",
    Condition.TARGET_ELEM_FLAME: "/icon/element/m/Icon_02_Flame.png",
    Condition.TARGET_ELEM_WATER: "/icon/element/m/Icon_02_Water.png",
    Condition.TARGET_ELEM_WIND: "/icon/element/m/Icon_02_Wind.png",
    Condition.TARGET_ELEM_LIGHT: "/icon/element/m/Icon_02_Light.png",
    Condition.TARGET_ELEM_SHADOW: "/icon/element/m/Icon_02_Dark.png",
}


def get_image_path(enum: TransformableEnums) -> Optional[str]:
    """
    Get the image path of ``enum``. Returns ``None`` if not found.

    The root directory of the path is ``assets/_gluonresources/resources/image``.

    The returned path will start with a slash "/".
    """
    return path_dict.get(enum)
