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
    TARGET_STORMLASHED = 113
    TARGET_SHADOWBLIGHTED = 114
    TARGET_SCORCHRENT = 115
    # endregion

    # region Elemental
    TARGET_ELEM_FLAME = 151
    TARGET_ELEM_WATER = 152
    TARGET_ELEM_WIND = 153
    TARGET_ELEM_LIGHT = 154
    TARGET_ELEM_SHADOW = 155
    # endregion

    # region State
    TARGET_BK_STATE = 180
    TARGET_OD_STATE = 181
    # endregion

    # region Abnormal
    TARGET_AFFLICTED = 191
    TARGET_DEF_DOWN = 192
    TARGET_BUFFED = 193
    TARGET_DEBUFFED = 194
    # endregion
    # endregion

    # region Self status
    # region HP
    SELF_HP_1 = 200
    """User's HP = 1."""
    SELF_HP_EQ_10 = 201
    """User's HP = 10% max."""
    SELF_HP_EQ_20 = 202
    """User's HP = 20% max."""
    SELF_HP_EQ_30 = 203
    """User's HP = 30% max."""
    SELF_HP_EQ_50 = 204
    """User's HP = 50% max."""
    SELF_HP_EQ_70 = 205
    """User's HP = 70% max."""
    SELF_HP_FULL = 206
    """User's HP is full."""

    SELF_HP_LT_40 = 210
    """User's HP < 40% max."""
    SELF_HP_LT_30 = 211
    """User's HP < 30% max."""

    SELF_HP_GT_30 = 220
    """User's HP > 30% max."""

    SELF_HP_GTE_40 = 225
    """User's HP >= 40% max."""
    SELF_HP_GTE_50 = 226
    """User's HP >= 50% max."""
    SELF_HP_GTE_60 = 227
    """User's HP >= 60% max."""
    SELF_HP_GTE_85 = 228
    """User's HP >= 85% max."""
    # endregion

    # region Combo count
    COMBO_0 = 240
    """User's combo count = 0."""
    COMBO_5 = 241
    """User's combo count = 5."""
    COMBO_10 = 242
    """User's combo count = 10."""
    COMBO_15 = 243
    """User's combo count = 15."""
    COMBO_20 = 244
    """User's combo count = 20."""
    COMBO_25 = 245
    """User's combo count = 25."""
    COMBO_30 = 246
    """User's combo count = 30."""
    # endregion

    # region Buff count
    SELF_BUFF_0 = 250
    SELF_BUFF_1 = 251
    SELF_BUFF_2 = 252
    SELF_BUFF_3 = 253
    SELF_BUFF_4 = 254
    SELF_BUFF_5 = 255
    SELF_BUFF_6 = 256
    SELF_BUFF_7 = 257
    SELF_BUFF_8 = 258
    SELF_BUFF_9 = 259
    SELF_BUFF_10 = 260
    SELF_BUFF_20 = 261
    SELF_BUFF_25 = 262
    SELF_BUFF_30 = 263
    SELF_BUFF_35 = 264
    SELF_BUFF_40 = 265
    SELF_BUFF_45 = 266
    SELF_BUFF_50 = 267
    # endregion

    # region In buff zone
    SELF_IN_BUFF_ZONE_BY_SELF_0 = 270
    SELF_IN_BUFF_ZONE_BY_SELF_1 = 271
    SELF_IN_BUFF_ZONE_BY_SELF_2 = 272
    SELF_IN_BUFF_ZONE_BY_ALLY_0 = 273
    SELF_IN_BUFF_ZONE_BY_ALLY_1 = 274
    SELF_IN_BUFF_ZONE_BY_ALLY_2 = 275
    SELF_IN_BUFF_ZONE_BY_ALLY_3 = 276
    # endregion

    # region Special status (for example, sigil locked for Nevin, guages filled for Gala Ranzal)
    SELF_SIGIL_LOCKED = 280  # ACID: 1152
    SELF_SIGIL_RELEASED = 281
    SELF_GAUGE_FILLED_0 = 282
    SELF_GAUGE_FILLED_1 = 283
    SELF_GAUGE_FILLED_2 = 284
    SELF_ENERGIZED = 290
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
    COVER_TEAMMATE_0 = 320
    COVER_TEAMMATE_1 = 321
    COVER_TEAMMATE_2 = 322
    COVER_TEAMMATE_3 = 323
    # endregion

    # region Bullets left on the map
    # EXNOTE: Only Meene uses this implementation for now, may be more in the future.
    # - Meene can only summon up to 9 butterflies on the map. This info has not yet been discovered by this parser.
    BULLETS_ON_MAP_0 = 330
    BULLETS_ON_MAP_1 = 331
    BULLETS_ON_MAP_2 = 332
    BULLETS_ON_MAP_3 = 333
    BULLETS_ON_MAP_4 = 334
    BULLETS_ON_MAP_5 = 335
    BULLETS_ON_MAP_6 = 336
    BULLETS_ON_MAP_7 = 337
    BULLETS_ON_MAP_8 = 338
    BULLETS_ON_MAP_9 = 339
    # endregion

    # region Additional inputs by user
    ADDL_INPUT_0 = 350
    ADDL_INPUT_1 = 351
    ADDL_INPUT_2 = 352
    ADDL_INPUT_3 = 353
    ADDL_INPUT_4 = 354
    ADDL_INPUT_5 = 355
    ADDL_INPUT_6 = 356
    # endregion

    # region Action canceling
    CANCELS_FJOACHIM_S2 = 370
    # endregion

    # region Miscellaneous
    MARK_EXPLODES = 390

    # endregion
    # endregion

    def __bool__(self):
        return self != SkillCondition.NONE

    def __lt__(self, other):
        if not isinstance(other, SkillCondition):
            raise TypeError(f"Cannot compare `SkillCondition` with type {type(other)}")

        return int(self.value) < int(other.value)
