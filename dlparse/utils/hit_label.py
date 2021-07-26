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


def make_hit_label(label: str, /, level: Optional[int] = None, shifted: Optional[bool] = None) -> str:
    """
    Make a hit label from ``label`` with specified properties.

    If ``label`` is not original, it will change to original label before processing,
    so the returned label is always valid.

    Nothing related will change if the corresponding property is not specified.
    """
    label_data = get_hit_label_data(label)
    label = label_data.original

    if shifted or (shifted is None and label_data.shifted):
        label += "_HAS"

    if label_lv := level or label_data.level:
        label += f"_LV{label_lv:02}"

    return label
