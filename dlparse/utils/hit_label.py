"""Utils for processing the hit attribute labels."""
from dataclasses import dataclass
from typing import Optional

__all__ = ("get_hit_label_data", "make_hit_label")


@dataclass
class HitLabelData:
    """A data class representing the attributes of a hit label."""

    raw: str

    original: str
    level: Optional[int]
    shifted: bool


def get_hit_label_data(label: str) -> HitLabelData:
    """Get the attributes of the hit ``label``."""
    parts = label.split("_")

    original_parts = []
    level = None
    shifted = False
    for part in parts:
        if part == "HAS" and not shifted:
            shifted = True
            continue

        if part.startswith("LV") and not level:
            level = int(part[2:])
            continue

        original_parts.append(part)

    return HitLabelData(raw=label, original="_".join(original_parts), level=level, shifted=shifted)


def make_hit_label(original: str, /, level: Optional[int] = None, shifted: Optional[bool] = None) -> str:
    """
    Make a hit label from the ``original`` label with specified properties.

    Nothing related will change if the corresponding property is not specified.
    """
    label = original

    if shifted:
        label += "_HAS"

    if level:
        label += f"_LV{level:02}"

    return label
