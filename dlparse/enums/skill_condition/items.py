"""Conditions for the skills."""
from enum import Enum

__all__ = ("SkillCondition",)


class SkillCondition(Enum):
    """
    Conditions for the skill data entries.

    .. note::
        Check https://github.com/PyCQA/pylint/issues/2306 for the reason of
        enum values being casted in the categorical check, although redundant.
    """

    NONE = 0

    # region Target
    # region Afflicted
    TARGET_POISONED = 101
    TARGET_BURNED = 102
    TARGET_FROZEN = 103
    TARGET_PARALYZED = 104
    TARGET_BLINDED = 105
    TARGET_STUNNED = 106
    TARGET_CURSED = 107
    TARGET_BOGGED = 109
    TARGET_SLEPT = 110
    TARGET_FROSTBITTEN = 111
    TARGET_FLASHBURNED = 112
    TARGET_CRASHWINDED = 113
    TARGET_SHADOWBLIGHTED = 114
    # endregion

    # region Elemental
    TARGET_ELEM_FLAME = 151
    TARGET_ELEM_WATER = 152
    TARGET_ELEM_WIND = 153
    TARGET_ELEM_LIGHT = 154
    TARGET_ELEM_SHADOW = 155
    # endregion
    # endregion

    # region Self status
    # region HP
    SELF_HP_1 = 201
    SELF_HP_FULL = 202
    # endregion

    # region Buff count
    SELF_BUFF_0 = 251
    SELF_BUFF_10 = 252
    SELF_BUFF_20 = 253
    SELF_BUFF_25 = 254
    SELF_BUFF_30 = 255
    SELF_BUFF_35 = 256
    SELF_BUFF_40 = 257
    SELF_BUFF_45 = 258
    SELF_BUFF_50 = 259
    # endregion
    # endregion

    # region Skill animation/effect
    # region Bullet hit count
    BULLET_HIT_1 = 301
    BULLET_HIT_2 = 302
    BULLET_HIT_3 = 303
    BULLET_HIT_4 = 304
    BULLET_HIT_5 = 305
    BULLET_HIT_6 = 306
    BULLET_HIT_7 = 307
    BULLET_HIT_8 = 308
    BULLET_HIT_9 = 309
    BULLET_HIT_10 = 310
    # endregion

    # region Count of teammates covered
    COVER_TEAMMATE_0 = 351
    COVER_TEAMMATE_1 = 352
    COVER_TEAMMATE_2 = 353
    COVER_TEAMMATE_3 = 354

    # endregion
    # endregion