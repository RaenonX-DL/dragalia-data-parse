"""Conditions for the skills."""
from enum import Enum
from functools import total_ordering

from ..mixin import TranslatableEnumMixin

__all__ = ("Condition",)


@total_ordering
class Condition(TranslatableEnumMixin, Enum):
    """
    Conditions for the skill data entries.

    .. note::
        Check https://github.com/PyCQA/pylint/issues/2306 for the reason of
        enum values being casted into int, although redundant.

        For all HP threshold handling, because the difference of having or not having equality in the comparison
        rarely impact the gameplay, therefore, all breakpoints with comparison are
        partitioned as either ``<`` (LT) or ``>=`` (GTE).
    """

    # WARNING: Codes are used by the website, DO NOT CHANGE

    NONE = 0

    # region 1xx - Target
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

    # region Element
    TARGET_FLAME = 151
    TARGET_WATER = 152
    TARGET_WIND = 153
    TARGET_LIGHT = 154
    TARGET_SHADOW = 155
    TARGET_ELEM_NEUTRAL = 157
    TARGET_ELEM_WEAK = 158
    TARGET_ELEM_EFFECTIVE = 159
    # endregion

    # region State
    TARGET_BK_STATE = 180
    TARGET_OD_STATE = 181
    # endregion

    # region Abnormal
    TARGET_AFFLICTED = 191
    TARGET_DEF_DOWN = 192
    TARGET_ATK_OR_DEF_DOWN = 195
    TARGET_BUFFED = 193
    TARGET_DEBUFFED = 194
    # endregion
    # endregion

    # region 2xx - Self status (general)
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

    SELF_HP_GTE_30 = 220
    """User's HP >= 30% max."""
    SELF_HP_GTE_40 = 225
    """User's HP >= 40% max."""
    SELF_HP_GTE_50 = 226
    """User's HP >= 50% max."""
    SELF_HP_GTE_60 = 227
    """User's HP >= 60% max."""
    SELF_HP_GTE_70 = 229
    """User's HP >= 70% max."""
    SELF_HP_GTE_80 = 224
    """User's HP >= 80% max."""
    SELF_HP_GTE_85 = 228
    """User's HP >= 85% max."""
    # endregion

    # region Combo count
    COMBO_GTE_0 = 240
    """User's combo count = 0."""
    COMBO_GTE_5 = 241
    """User's combo count = 5."""
    COMBO_GTE_10 = 242
    """User's combo count = 10."""
    COMBO_GTE_15 = 243
    """User's combo count = 15."""
    COMBO_GTE_20 = 244
    """User's combo count = 20."""
    COMBO_GTE_25 = 245
    """User's combo count = 25."""
    COMBO_GTE_30 = 246
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
    SELF_BUFF_15 = 261
    SELF_BUFF_20 = 262
    SELF_BUFF_25 = 263
    SELF_BUFF_30 = 264
    SELF_BUFF_35 = 265
    SELF_BUFF_40 = 266
    SELF_BUFF_45 = 267
    SELF_BUFF_50 = 268
    # endregion

    # region In buff field
    IN_BUFF_FIELD_BY_SELF_0 = 270
    IN_BUFF_FIELD_BY_SELF_1 = 271
    IN_BUFF_FIELD_BY_SELF_2 = 272
    IN_BUFF_FIELD_BY_ALLY_0 = 273
    IN_BUFF_FIELD_BY_ALLY_1 = 274
    IN_BUFF_FIELD_BY_ALLY_2 = 275
    IN_BUFF_FIELD_BY_ALLY_3 = 276
    # endregion

    # region Weapon type
    WEAPON_SWORD = 291
    WEAPON_BLADE = 292
    WEAPON_DAGGER = 293
    WEAPON_AXE = 294
    WEAPON_LANCE = 295
    WEAPON_BOW = 296
    WEAPON_ROD = 297
    WEAPON_STAFF = 298
    WEAPON_MANACASTER = 299
    # endregion
    # endregion

    # region 3xx - Skill animation/effect
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
    #   - Meene can only summon up to 9 butterflies on the map. This info has not yet been discovered by this parser.
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

    # region Miscellaneous variant
    MARK_EXPLODES = 390
    COUNTER_RED_ATTACK = 391
    # endregion
    # endregion

    # region 4xx - Self status (special)
    # region Action condition (Sigil released, lapis cards, etc.)
    SELF_SIGIL_LOCKED = 400  # ACID: 1152
    SELF_SIGIL_RELEASED = 401
    SELF_SMIKOTO_CEL_SUN_WAVE = 402  # ACID: 977 (Sun) / 978 (Wave)
    SELF_GLEONIDAS_FULL_STACKS = 403  # ACID: 1380
    SELF_SEIMEI_SHIKIGAMI_LV_1 = 404
    SELF_SEIMEI_SHIKIGAMI_LV_2 = 405
    SELF_LAPIS_CARD_0 = 410  # ACID: 1319
    SELF_LAPIS_CARD_1 = 411  # ACID: 1319
    SELF_LAPIS_CARD_2 = 412  # ACID: 1319
    SELF_LAPIS_CARD_3 = 413  # ACID: 1319
    SELF_SMYM_COMBO_BOOSTED = 414  # ACID: 1768
    SELF_SMYM_COMBO_NOT_BOOSTED = 415  # ACID: 1768
    SELF_GMASCULA_S1_LV1 = 416  # ACID: 1750
    SELF_GMASCULA_S1_LV2 = 417  # ACID: 1751
    SELF_GMASCULA_S1_LV3 = 418  # ACID: 1752
    # endregion

    # region Action condition level
    ACTION_COND_LV_1 = 441
    ACTION_COND_LV_2 = 442
    ACTION_COND_LV_3 = 443
    ACTION_COND_LV_4 = 444
    ACTION_COND_LV_5 = 445
    # endregion

    # region Gauge-related
    SELF_GAUGE_FILLED_0 = 450
    SELF_GAUGE_FILLED_1 = 451
    SELF_GAUGE_FILLED_2 = 452
    # endregion

    # region Dragon / Shapeshift
    SELF_SHAPESHIFTED_1_TIME = 471
    SELF_SHAPESHIFTED_2_TIMES = 472
    SELF_SHAPESHIFTED_3_TIMES = 473
    SELF_SHAPESHIFTED_1_TIME_IN_DRAGON = 475
    SELF_SHAPESHIFTED_2_TIMES_IN_DRAGON = 476
    SELF_SHAPESHIFT_COMPLETED = 478
    # endregion

    # region Skill usage
    SKILL_USED_S1 = 481
    SKILL_USED_S2 = 482
    SKILL_USED_ALL = 489
    # endregion

    # region Special (Energized, inspired, amp)
    SELF_ENERGIZED = 490
    SELF_TEAM_AMP_UP = 491
    # endregion
    # endregion

    # region 8xx - Trigger
    # region Effect triggered by self
    # region Miscellaneoous
    ON_BUFFED_DEF = 801
    ON_REVIVED = 802
    ON_ENERGY_LV_UP = 803
    ON_ENTERED_BUFF_FIELD = 804
    ON_HEALED = 805
    ON_DODGE_SUCCESS = 806
    # endregion

    # region HP change
    ON_HP_LT_30 = 810
    ON_HP_LT_40 = 811
    ON_HP_LT_60 = 812
    ON_HP_GTE_40 = 820
    ON_HP_GTE_60 = 821
    # endregion

    # region Infliction
    ON_INFLICTED_POISON = 831
    ON_INFLICTED_BURN = 832
    ON_INFLICTED_FREEZE = 833
    ON_INFLICTED_PARALYZE = 834
    ON_INFLICTED_BLIND = 835
    ON_INFLICTED_STUN = 836
    ON_INFLICTED_CURSE = 837
    ON_INFLICTED_BOG = 839
    ON_INFLICTED_SLEEP = 840
    ON_INFLICTED_FROSTBITE = 841
    ON_INFLICTED_FLASHBURN = 842
    ON_INFLICTED_STORMLASH = 843
    ON_INFLICTED_SHADOWBLIGHT = 844
    ON_INFLICTED_SCORCHREND = 845
    # endregion

    # region Combo count
    ON_COMBO_RESET = 850
    ON_COMBO_GTE_10 = 851
    ON_COMBO_DIV_BY_10 = 855
    ON_COMBO_DIV_BY_20 = 856
    ON_COMBO_DIV_BY_50 = 857
    # endregion
    # endregion

    # region Effect triggered by others
    ON_HIT = 860
    ON_HIT_BY_POISON = 861
    ON_HIT_BY_BURN = 862
    ON_HIT_BY_FREEZE = 863
    ON_HIT_BY_PARALYZE = 864
    ON_HIT_BY_BLIND = 865
    ON_HIT_BY_STUN = 866
    ON_HIT_BY_CURSE = 867
    ON_HIT_BY_BOG = 869
    ON_HIT_BY_SLEEP = 870
    ON_HIT_BY_FROSTBITE = 871
    ON_HIT_BY_FLASHBURN = 872
    ON_HIT_BY_STORMLASH = 873
    ON_HIT_BY_SHADOWBLIGHT = 874
    ON_HIT_BY_SCORCHREND = 875
    ON_HIT_BY_ANY_AFFLICTION = 881
    # endregion
    # endregion

    # region 9xx - Miscellaneous (e.g. quest start)
    QUEST_START = 901

    # region Probabilistic
    PROB_25 = 910
    PROB_33 = 911
    PROB_50 = 912
    PROB_67 = 913
    PROB_75 = 914

    # endregion
    # endregion

    @property
    def translation_id(self) -> str:
        return f"ENUM_COND_{self.name}"

    @staticmethod
    def get_all_translatable_members() -> list["Condition"]:
        return list(Condition)

    def __bool__(self):
        return self != Condition.NONE

    def __lt__(self, other):
        if not isinstance(other, Condition):
            raise TypeError(f"Cannot compare `Condition` with type {type(other)}")

        return int(self.value) < int(other.value)
