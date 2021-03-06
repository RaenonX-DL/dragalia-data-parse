"""Class for ``ActionPartsSettingHit`` action component."""
from dataclasses import dataclass
from typing import Union

from dlparse.mono.asset.base import ActionComponentHasHitLabels

__all__ = ("ActionSettingHit",)


@dataclass
class ActionSettingHit(ActionComponentHasHitLabels):
    """Class of ``ActionPartsSettingHit`` component in the player action asset."""

    field_lifetime: float

    @classmethod
    def parse_raw(cls, data: dict[str, Union[str, float]]) -> "ActionSettingHit":
        kwargs = cls.get_base_kwargs(data)

        return ActionSettingHit(
            hit_labels=[data["_hitAttrLabel"]],
            field_lifetime=data["_lifetime"],
            **kwargs
        )
