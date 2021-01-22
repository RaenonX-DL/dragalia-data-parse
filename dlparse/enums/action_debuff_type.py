"""Debuff type enum."""
from enum import Enum

__all__ = ("ActionDebuffType",)


class ActionDebuffType(Enum):
    """
    Enums of the debuff types.

    This is used by the ability condition fields, where if the condition type is ``DEBUFF`` (``50``),
    the condition value will be this.

    The enum definition can be found in ``Gluon.CharacterBuff.ActionDefDebuff`` in the metadata.
    """

    UNKNOWN = -1

    DEF_DOWN = 3
    ATK_OR_DEF_DOWN = 21

    @classmethod
    def _missing_(cls, _):
        return ActionDebuffType.UNKNOWN
