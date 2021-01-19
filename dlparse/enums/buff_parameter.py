"""Buff parameter enum class."""
from enum import Enum

__all__ = ("BuffParameter",)


class BuffParameter(Enum):
    """
    Buff target parameter enum class.

    The number is arbitrarily defined (not appeared in the game asset).
    """

    # WARNING: The number should not be changed frequently because the changes need to be reflected at the frontend

    # region Common
    ATK = 101
    """ATK up. A value of 0.12 means ATK +12%."""
    DEF = 102
    """DEF up. A value of 0.12 means DEF +12%."""
    CRT_RATE = 103
    """Critical rate up. A value of 0.12 means CRT +12%."""
    CRT_DAMAGE = 104
    """Critical damage up. A value of 0.12 means CRT DMG +12%."""
    SKILL_DAMAGE = 105
    """Skill damage up. A value of 0.12 means SDMG +12%."""
    ATK_SPD = 106
    """Attack speed up. A value of 0.12 means ASPD +12%."""
    FS_DAMAGE = 107
    """Force strike damage up. A value of 0.12 means FS DMG +12%."""
    FS_SPD = 108
    """Force strike charging speed up. A value of 0.12 means FS SPD +12%."""
    # endregion

    # region SP Control
    SP_RATE = 201
    """Rate of SP gain. A value of 0.12 means SP +12%."""
    SP_GAIN = 202
    """Immediate SP gain. A value of 100 means get SP 100."""
    SP_CHARGE_PCT_S1 = 211
    """
    Immediately charges the SP of **S1**.

    A value of 0.15 means to refill 15% SP of S1.
    """
    SP_CHARGE_PCT_S2 = 212
    """
    Immediately charges the SP of **S2**.

    A value of 0.15 means to refill 15% SP of S2.
    """
    SP_CHARGE_PCT_S3 = 213
    """
    Immediately charges the SP of **S3**.

    A value of 0.15 means to refill 15% SP of S3.
    """
    SP_CHARGE_PCT_S4 = 214
    """
    Immediately charges the SP of **S4**.

    A value of 0.15 means to refill 15% SP of S4.
    """
    SP_CHARGE_PCT_USED = 215
    """
    Immediately charges the SP of the skill that was just used.

    A value of 0.15 means to refill 15% SP of the skill used.
    """
    # endregion

    # region Recovery
    HEAL_RP = 301
    """Heal the target using Recovery Potency. A value of 0.12 means that the target will be healed with 12% RP."""
    # endregion

    # region Defensive
    # region Shield
    SHIELD_SINGLE_DMG = 401
    """
    Shield that nullfies a damage according to the user's max HP once.

    A value of 0.12 means that the shield nullfies a damage which is less than 12% of the user's max HP.

    Note that this shield is unstackable and will disappear once the user got hit.
    """
    SHIELD_LIFE = 402
    """
    Shield that nullifies a damage equal to the amount of HP that should lost.

    A value of 0.3 means that the user will lost their HP until 30% of the max. The lost HP will become the shield.

    Check https://dragalialost.gamepedia.com/Life_Shield for more details.
    """
    # endregion

    # region Element Resistance
    RESISTANCE_FLAME = 411
    """Flame resistance up. A value of 0.12 means that the user reduces flame damage taken by 12%."""
    RESISTANCE_WATER = 412
    """Water resistance up. A value of 0.12 means that the user reduces water damage taken by 12%."""
    RESISTANCE_WIND = 413
    """Wind resistance up. A value of 0.12 means that the user reduces wind damage taken by 12%."""
    RESISTANCE_LIGHT = 414
    """Light resistance up. A value of 0.12 means that the user reduces light damage taken by 12%."""
    RESISTANCE_SHADOW = 415
    """Shadow resistance up. A value of 0.12 means that the user reduces shadow damage taken by 12%."""
    # endregion

    # region Affliction Resistance
    RESISTANCE_POISON = 431
    """Poison resistance up. A value of 0.12 means that the probability of being posioned is reduced by 12%."""
    RESISTANCE_BURN = 432
    """Burn resistance up. A value of 0.12 means that the probability of being burned is reduced by 12%."""
    RESISTANCE_FREEZE = 433
    """Freeze resistance up. A value of 0.12 means that the probability of being frozen is reduced by 12%."""
    RESISTANCE_PARALYZE = 434
    """Paralyze resistance up. A value of 0.12 means that the probability of being paralyzed is reduced by 12%."""
    RESISTANCE_BLIND = 435
    """Blind resistance up. A value of 0.12 means that the probability of being blinded is reduced by 12%."""
    RESISTANCE_STUN = 436
    """Stun resistance up. A value of 0.12 means that the probability of being stunned is reduced by 12%."""
    RESISTANCE_CURSE = 437
    """Curse resistance up. A value of 0.12 means that the probability of being cursed is reduced by 12%."""
    RESISTANCE_BOG = 439
    """Bog resistance up. A value of 0.12 means that the probability of being bogged is reduced by 12%."""
    RESISTANCE_SLEEP = 440
    """Sleep resistance up. A value of 0.12 means that the probability of being slept is reduced by 12%."""
    RESISTANCE_FROSTBITE = 441
    """Frostbite resistance up. A value of 0.12 means that the probability of being frostbitten is reduced by 12%."""
    RESISTANCE_FLASHBURN = 442
    """Flashburn resistance up. A value of 0.12 means that the probability of being flashburned is reduced by 12%."""
    RESISTANCE_STORMLASH = 443
    """Stormlash resistance up. A value of 0.12 means that the probability of being stormlashed is reduced by 12%."""
    RESISTANCE_SHADOWBLIGHT = 444
    """
    Shadowblight resistance up.

    A value of 0.12 means that the probability of being shadowblighted is reduced by 12%.
    """
    RESISTANCE_SCORCHREND = 445
    """Scorchrend resistance up. A value of 0.12 means that the probability of being scorchrent is reduced by 12%."""
    # endregion
    # endregion

    # region HP Control
    HP_FIX_BY_MAX = 501
    """
    Directly fixes HP by a certain rate.

    A value of 0.12 means the user's HP will be set to 12% of the max.
    """
    HP_DECREASE_BY_MAX = 502
    """
    Decreases HP by a certain rate.

    A value of 0.12 means to decrease 12% HP.
    """
    HP_RAISE_BY_MAX = 503
    """
    Increases max HP by a certain rate.

    A value of 0.12 means to increase the max HP by 12%.
    """
    # endregion

    # region Dragon Control
    DRAGON_TIME = 601
    """
    Increases the shapeshifting duration by a certain rate.

    A value of 0.12 means to increase the shapeshifting duration by 12% (for example, 10s to 11.2s).
    """
    DRAGON_TIME_FINAL = 602
    """
    Change the shapeshifting duration after calculating `DRAGON_TIME`.

    A value of 0.12 means to add 12% shapeshifting duration after calculating `DRAGON_TIME`.

    If the original shapeshifting duration is 10s, `DRAGON_TIME` is 0.5 (+50%) and `DRAGON_TIME_FINAL` is 0.25 (+25%),
    the duration will then becomes 18.75s (10 * (1 + 0.5) * (1 + 0.25)), instead of 17.5s (10 + (1 + 0.5 + 0.25)).
    """
    DP_CONSUMPTION = 603
    """
    Change the dragon gauge consumption for shapeshifting.

    A value of 0.2 means that to increase the gauge consumption by 20%, which means that to shapeshift once,
    70% of the dragon gauge is required (shapeshifting once consume 50% dragon gauge).
    """
    # endregion

    # region Special Sentinel
    AFFLICTION = 901
    """The buff is an affliction. Value does not have any meanings."""
    MARK = 902
    """The buff is a mark. Value does not have any meanings. This is used by Nobunaga only as of 2020/12/10."""
    # endregion
