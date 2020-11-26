"""Class for ``ActionPartsSettingHit`` action component."""
from dataclasses import dataclass
from typing import Union

from dlparse.mono.asset.base import ActionComponentDamageDealer


@dataclass
class ActionSettingHit(ActionComponentDamageDealer):
    """Class of ``ActionPartsSettingHit`` component in the player action asset."""

    area_lifetime: float

    @classmethod
    def parse_raw(cls, data: dict[str, Union[str, float]]) -> "ActionSettingHit":
        kwargs = cls.get_base_kwargs(data)

        return ActionSettingHit(
            hit_labels=[data["_hitLabel"]],
            area_lifetime=data["_lifetime"],
            **kwargs
        )
