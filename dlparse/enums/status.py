"""Status enums."""
from enum import IntEnum

from dlparse.errors import EnumConversionError
from .buff_parameter import BuffParameter

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
    REBORN = 8  # `AbsRebirth = 8` officially
    BOG = 9
    SLEEP = 10
    FROSTBITE = 11
    FLASHBURN = 12
    STORMLASH = 13
    SHADOWBLIGHT = 14
    SCORCHREND = 15

    AFFLICTED = 99

    HP_DOWNED = 101
    ATK_DOWNED = 102
    DEF_DOWNED = 103
    CRT_DOWNED = 104
    SKILL_DMG_DOWNED = 105
    FS_DMG_DOWNED = 106
    RP_DOWNED = 107
    BLEEDING = 108

    BUFFED_OR_DEBUFFED = 197
    BUFFED = 198
    DEBUFFED = 199

    BK_STATE = 201

    @property
    def is_abnormal_status(self):
        """Check if the status is one of the abnormal statuses."""
        # Assumes that 16~20 (not yet used as of 2020/12/05) will still be abnormal status
        return 1 <= int(self.value) <= 20

    @property
    def icon_name(self) -> str:
        """Get the file name of the status icon, excluding the file extension."""
        return f"Icon_Status_01_{self.value:02}"

    def to_buff_param_resist(self) -> BuffParameter:
        """
        Convert the current status to resistance buff parameter.

        :raises EnumConversionError: if the current status cannot be converted to resistance buff parameter
        """
        if self not in _TRANS_DICT_RESIST:
            raise EnumConversionError(self, Status, BuffParameter)

        return _TRANS_DICT_RESIST[self]

    def to_buff_param_inflict(self) -> BuffParameter:
        """
        Convert the current status to infliction probability buff parameter.

        :raises EnumConversionError: if the current status cannot be converted to infliction probability buff parameter
        """
        if self not in _TRANS_DICT_INFLICT:
            raise EnumConversionError(self, Status, BuffParameter)

        return _TRANS_DICT_INFLICT[self]

    def to_buff_param_punisher(self) -> BuffParameter:
        """
        Convert the current status to punisher buff parameter.

        :raises EnumConversionError: if the current status cannot be converted to punisher buff parameter
        """
        if self not in _TRANS_DICT_PUNISHER:
            raise EnumConversionError(self, Status, BuffParameter)

        return _TRANS_DICT_PUNISHER[self]


_TRANS_DICT_RESIST: dict[Status, BuffParameter] = {
    Status.POISON: BuffParameter.RESISTANCE_POISON,
    Status.BURN: BuffParameter.RESISTANCE_BURN,
    Status.FREEZE: BuffParameter.RESISTANCE_FREEZE,
    Status.PARALYZE: BuffParameter.RESISTANCE_PARALYZE,
    Status.BLIND: BuffParameter.RESISTANCE_BLIND,
    Status.STUN: BuffParameter.RESISTANCE_STUN,
    Status.CURSE: BuffParameter.RESISTANCE_CURSE,
    Status.BOG: BuffParameter.RESISTANCE_BOG,
    Status.SLEEP: BuffParameter.RESISTANCE_SLEEP,
    Status.FROSTBITE: BuffParameter.RESISTANCE_FROSTBITE,
    Status.FLASHBURN: BuffParameter.RESISTANCE_FLASHBURN,
    Status.STORMLASH: BuffParameter.RESISTANCE_STORMLASH,
    Status.SHADOWBLIGHT: BuffParameter.RESISTANCE_SHADOWBLIGHT,
    Status.SCORCHREND: BuffParameter.RESISTANCE_SCORCHREND
}

_TRANS_DICT_INFLICT: dict[Status, BuffParameter] = {
    Status.POISON: BuffParameter.INFLICT_PROB_POISON,
    Status.BURN: BuffParameter.INFLICT_PROB_BURN,
    Status.FREEZE: BuffParameter.INFLICT_PROB_FREEZE,
    Status.PARALYZE: BuffParameter.INFLICT_PROB_PARALYZE,
    Status.BLIND: BuffParameter.INFLICT_PROB_BLIND,
    Status.STUN: BuffParameter.INFLICT_PROB_STUN,
    Status.CURSE: BuffParameter.INFLICT_PROB_CURSE,
    Status.BOG: BuffParameter.INFLICT_PROB_BOG,
    Status.SLEEP: BuffParameter.INFLICT_PROB_SLEEP,
    Status.FROSTBITE: BuffParameter.INFLICT_PROB_FROSTBITE,
    Status.FLASHBURN: BuffParameter.INFLICT_PROB_FLASHBURN,
    Status.STORMLASH: BuffParameter.INFLICT_PROB_STORMLASH,
    Status.SHADOWBLIGHT: BuffParameter.INFLICT_PROB_SHADOWBLIGHT,
    Status.SCORCHREND: BuffParameter.INFLICT_PROB_SCORCHREND
}

_TRANS_DICT_PUNISHER: dict[Status, BuffParameter] = {
    Status.POISON: BuffParameter.POISONED_PUNISHER,
    Status.BURN: BuffParameter.BURNED_PUNISHER,
    Status.FREEZE: BuffParameter.FROZEN_PUNISHER,
    Status.PARALYZE: BuffParameter.PARALYZED_PUNISHER,
    Status.BLIND: BuffParameter.BLINDED_PUNISHER,
    Status.STUN: BuffParameter.STUNNED_PUNISHER,
    Status.CURSE: BuffParameter.CURSED_PUNISHER,
    Status.BOG: BuffParameter.BOGGED_PUNISHER,
    Status.SLEEP: BuffParameter.SLEPT_PUNISHER,
    Status.FROSTBITE: BuffParameter.FROSTBITTEN_PUNISHER,
    Status.FLASHBURN: BuffParameter.FLASHBURNED_PUNISHER,
    Status.STORMLASH: BuffParameter.STORMLASHED_PUNISHER,
    Status.SHADOWBLIGHT: BuffParameter.SHADOWBLIGHTED_PUNISHER,
    Status.SCORCHREND: BuffParameter.SCORCHRENT_PUNISHER
}
