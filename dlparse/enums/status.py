"""Status enums."""
from enum import IntEnum

__all__ = ("Status",)


class Status(IntEnum):
    """
    Enums used in the assets to represent the status. Different context may have different meaning toward this.

    This corresponds to:

    - Field ``_KillerState1``, ``_KillerState2`` and ``_KillerState3`` in the hit attribute asset.

        In this context, this means that if the target has any of the status listed in the fields above,
        bonus damage rate will be applied.

    - Field ``_Type`` in the action condition asset.

        In this context, this means that the action condition will gives the particular affliction.

        A special case where ``_Type`` is ``99`` (``AFFLICTED``) means that all abnormal statuses will be removed.
    """

    UNKNOWN = -1

    NONE = 0
    POISON = 1
    BURN = 2
    FREEZE = 3
    PARALYZE = 4
    BLIND = 5
    STUN = 6
    CURSE = 7
    BOG = 9
    SLEEP = 10
    FROSTBITE = 11
    FLASHBURN = 12
    CRASHWIND = 13
    SHADOWBLIGHT = 14

    AFFLICTED = 99

    DEF_DOWNED = 103
    BUFFED = 198
    DEBUFFED = 199

    BREAK_STATE = 201

    @property
    def is_abnormal_status(self):
        """Check if the status is one of the abnormal statuses."""
        # Assumes that 16~20 (not yet used as of 2020/12/05) will still be abnormal status
        return 1 <= int(self.value) <= 20
