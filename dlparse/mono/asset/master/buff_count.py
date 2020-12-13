"""Classes for handling the buff count data asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import SkillConditionCategories, SkillConditionComposite
from dlparse.errors import AppValueError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("BuffCountEntry", "BuffCountAsset", "BuffCountParser")


@dataclass
class BuffCountEntry(MasterEntryBase):
    """Single entry of a buff count data."""

    rate_limit: float
    rate_base: float

    action_condition_id: int
    action_condition_rate: float

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "BuffCountEntry":
        return BuffCountEntry(
            id=data["_Id"],
            rate_limit=data["_LimitRate"],
            rate_base=data["_BaseRate"],
            action_condition_id=data["_Condition1Id"],
            action_condition_rate=data["_Condition1Rate"],
        )

    def get_effective_action_condition_count(self, cond_comp: SkillConditionComposite) -> int:
        """Get the count of effective action condition instances."""
        if self.action_condition_id != cond_comp.action_cond_id:
            # ACID in `cond_comp` is not the action condition for extra boost
            return 0

        action_cond_cat = SkillConditionCategories.get_category_action_condition(cond_comp.action_cond_id)
        action_cond_item = action_cond_cat.extract(cond_comp)
        action_cond_conv = action_cond_cat.convert(action_cond_item)

        if not isinstance(action_cond_conv, int):
            # Extracted and converted skill condition is not an integer
            raise AppValueError(
                f"Converted condition {action_cond_item} of action condition #{cond_comp.action_cond_id} "
                f"is not an integer: {type(action_cond_conv)} {action_cond_conv}"
            )

        return action_cond_conv

    def get_buff_up_rate(self, cond_comp: SkillConditionComposite) -> float:
        """Get the effective buff up rate according to the given skill condition."""
        rate: float = 0

        # Multiply base rate using the buff count from condition composite (if any)
        if buff_count := cond_comp.buff_count_converted:
            rate += buff_count * self.rate_base

        # Multiply action condition rate if the condition has matching one
        if cond_comp.action_cond_id == self.action_condition_id:
            rate += self.get_effective_action_condition_count(cond_comp) * self.action_condition_rate

        # Cap the buff up rate
        return min(rate, self.rate_limit)


class BuffCountAsset(MasterAssetBase[BuffCountEntry]):
    """Buff count data asset class."""

    asset_file_name = "BuffCountData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(BuffCountParser, file_location, asset_dir=asset_dir, file_like=file_like)


class BuffCountParser(MasterParserBase[BuffCountEntry]):
    """Class to parse the buff count data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, BuffCountEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: BuffCountEntry.parse_raw(value) for key, value in entries.items()}
