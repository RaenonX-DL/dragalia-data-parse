"""Extension for some parameter that changes depends on the user's combo count."""
from dataclasses import InitVar, dataclass, field
from typing import Optional

from dlparse.enums import Condition, ConditionCategories

__all__ = ("ComboBoostValueExtension",)


@dataclass
class ComboBoostValueExtension:
    """A class storing a certain parameter that changes according to the user's combo count."""

    raw_data: InitVar[Optional[str]] = None

    combo_boost_data: list[tuple[int, float]] = field(default_factory=list)
    conditions: list[Condition] = field(default_factory=list)

    def __post_init__(self, raw_data: Optional[str]):
        if not raw_data:
            # `raw_data` is an empty string, no combo data
            return

        for entry in raw_data.split("/"):
            combo_count, value = entry.split("_")
            combo_count = int(combo_count)

            self.combo_boost_data.append((combo_count, float(value)))
            self.conditions.append(ConditionCategories.self_combo_count.convert_reversed(combo_count))

    def get_value_by_combo(self, combo_count: int) -> float:
        """Get the value when the user's combo count is ``combo_count``."""
        # Highest combo threshold first, reversing the data list
        for min_combo_count, value in reversed(self.combo_boost_data):
            if combo_count >= min_combo_count:
                return value

        return 0

    @property
    def is_effective(self) -> bool:
        """If the combo boost data is effective."""
        return bool(self.combo_boost_data)
