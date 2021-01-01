"""Function to export the elemental bonus data."""
import json
import os

from dlparse.enums import Condition, Element

__all__ = ("export_elem_bonus_as_json",)

# Hard-coded the data to be exported to avoid unnecessary implementations,
# because this almost never change.

elem_bonus_data_template = {
    Condition.TARGET_ELEM_FLAME.value: 1,
    Condition.TARGET_ELEM_WATER.value: 1,
    Condition.TARGET_ELEM_WIND.value: 1,
    Condition.TARGET_ELEM_LIGHT.value: 1,
    Condition.TARGET_ELEM_SHADOW.value: 1,
    Condition.TARGET_ELEM_WEAK.value: 0.5,
    Condition.TARGET_ELEM_EFFECTIVE.value: 1.5,
    Condition.TARGET_ELEM_NEUTRAL.value: 1,
}

elem_bonus_data = {
    Element.N_A.value: elem_bonus_data_template,
    Element.NO_ELEMENT.value: elem_bonus_data_template,
    Element.FLAME.value: elem_bonus_data_template | {
        Condition.TARGET_ELEM_WATER.value: 0.5,
        Condition.TARGET_ELEM_WIND.value: 1.5,
    },
    Element.WATER.value: elem_bonus_data_template | {
        Condition.TARGET_ELEM_WIND.value: 0.5,
        Condition.TARGET_ELEM_FLAME.value: 1.5,
    },
    Element.WIND.value: elem_bonus_data_template | {
        Condition.TARGET_ELEM_FLAME.value: 0.5,
        Condition.TARGET_ELEM_WATER.value: 1.5,
    },
    Element.LIGHT.value: elem_bonus_data_template | {
        Condition.TARGET_ELEM_SHADOW.value: 1.5,
    },
    Element.SHADOW.value: elem_bonus_data_template | {
        Condition.TARGET_ELEM_LIGHT.value: 1.5,
    },
}


def export_elem_bonus_as_json(file_path: str):
    """Export the element bonus data as a json file to ``file_path``."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if needed

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        json.dump(elem_bonus_data, f, ensure_ascii=False)