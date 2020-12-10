"""Class for ``ActionPartsRemoveBuffTriggerBomb`` action component."""
from dataclasses import dataclass
from typing import Union

from dlparse.enums import SkillCondition
from dlparse.errors import PreconditionCollidedError
from dlparse.mono.asset.base import ActionComponentHasHitLabels

__all__ = ("ActionBuffBomb",)


@dataclass
class ActionBuffBomb(ActionComponentHasHitLabels):
    """Class of ``ActionPartsRemoveBuffTriggerBomb`` component in the player action asset."""

    action_condition_id: int

    @property
    def skill_pre_condition(self) -> SkillCondition:
        if super().skill_pre_condition:
            raise PreconditionCollidedError(SkillCondition.MARK_EXPLODES, super().skill_pre_condition)

        return SkillCondition.MARK_EXPLODES

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBuffBomb":
        kwargs = cls.get_base_kwargs(data)

        return ActionBuffBomb(
            hit_labels=[data["_hitAttrLabel"]],
            action_condition_id=data["_targetActionConditionId"],
            **kwargs
        )
