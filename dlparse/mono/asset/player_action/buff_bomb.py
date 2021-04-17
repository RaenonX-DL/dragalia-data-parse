"""Class for ``ActionPartsRemoveBuffTriggerBomb`` action component."""
from dataclasses import dataclass

from dlparse.enums import Condition
from dlparse.errors import PreconditionCollidedError
from dlparse.mono.asset.base import ActionComponentData, ActionComponentHasHitLabels

__all__ = ("ActionBuffBomb",)


@dataclass
class ActionBuffBomb(ActionComponentHasHitLabels):
    """Class of ``ActionPartsRemoveBuffTriggerBomb`` component in the player action asset."""

    action_condition_id: int

    @property
    def skill_pre_condition(self) -> Condition:
        if super().skill_pre_condition:
            raise PreconditionCollidedError(Condition.MARK_EXPLODES, super().skill_pre_condition)

        return Condition.MARK_EXPLODES

    @classmethod
    def parse_raw(cls, data: ActionComponentData) -> "ActionBuffBomb":
        kwargs = cls.get_base_kwargs(data)

        return ActionBuffBomb(
            hit_labels=[data["_hitAttrLabel"]],
            action_condition_id=data["_targetActionConditionId"],
            **kwargs
        )
