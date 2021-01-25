"""Buff parameter enum class."""
from enum import Enum

from .mixin import TranslatableEnumMixin

__all__ = ("BuffParameter", "BuffValueUnit")


class BuffValueUnit(TranslatableEnumMixin, Enum):
    """Enums for the unit of the buff parameter value."""

    NONE = 0
    PERCENTAGE = 1
    SECONDS = 2
    SKILL_POINT = 3
    LEVEL = 4

    @property
    def translation_id(self) -> str:
        return f"ENUM_UNIT_{self.name}"

    @staticmethod
    def get_all_translatable_members() -> list["BuffValueUnit"]:
        return [
            BuffValueUnit.NONE,
            BuffValueUnit.PERCENTAGE,
            BuffValueUnit.SECONDS,
            BuffValueUnit.SKILL_POINT,
            BuffValueUnit.LEVEL
        ]


class BuffParameter(TranslatableEnumMixin, Enum):
    """
    Buff target parameter enum class.

    The number is arbitrarily defined (not appeared in the game asset).
    """

    # WARNING: The number should not be changed frequently because the changes need to be reflected at the frontend

    # region General (to Self)
    # region Buff / Undistinguished
    ATK_BUFF = 101
    """ATK up (calculated as buff). A value of 0.12 means ATK +12%."""
    DEF_BUFF = 102
    """DEF up (calculated as buff). A value of 0.12 means DEF +12%."""
    CRT_RATE_BUFF = 103
    """Critical rate up (calculated as buff). A value of 0.12 means CRT +12%."""
    CRT_DAMAGE_BUFF = 104
    """Critical damage up (calculated as buff). A value of 0.12 means CRT DMG +12%."""
    SKILL_DAMAGE_BUFF = 105
    """Skill damage up (calculated as buff). A value of 0.12 means SDMG +12%."""
    ASPD_BUFF = 106
    """Attack speed up (calculated as buff). A value of 0.12 means ASPD +12%."""
    FS_DAMAGE_BUFF = 107
    """Force strike damage up (calculated as buff). A value of 0.12 means FS DMG +12%."""
    FS_SPD = 108
    """Force strike charging speed up (calculated as buff). A value of 0.12 means FS SPD +12%."""
    OD_GAUGE_DAMAGE = 109
    """Deals more damage to the OD gauge. A value of 0.12 means OD gauge damage +12%."""
    AUTO_DAMAGE = 110
    """Auto damage up. A value of 0.12 means auto / normal attack damage +12%."""
    TARGETED_BUFF_TIME = 111
    """
    Targeted buff time extension. A value of 0.12 means buff time +12%.

    Note that the "targeted" here means that the extension is only effective to the buff that targets the players,
    such as ATK up buffs.
    The duration of the buff field like the one built by Gala Euden S1 (101504031) will **not** be affected by this.
    """
    COMBO_TIME = 112
    """
    Combo counter valid time extension.

    A value of 2.5 means combo counter will not reset for additional 2.5 seconds.
    """
    # endregion

    # region Elemental
    FLAME_ELEM_DMG_UP = 120
    """Flame elemental damage up. A value of 0.12 means flame elemental damage +12%."""
    WATER_ELEM_DMG_UP = 121
    """Water elemental damage up. A value of 0.12 means water elemental damage +12%."""
    WIND_ELEM_DMG_UP = 122
    """Wind elemental damage up. A value of 0.12 means wind elemental damage +12%."""
    LIGHT_ELEM_DMG_UP = 123
    """Light elemental damage up. A value of 0.12 means light elemental damage +12%."""
    SHADOW_ELEM_DMG_UP = 124
    """Shadow elemental damage up. A value of 0.12 means shadow elemental damage +12%."""
    # endregion

    # region Passive
    ATK_PASSIVE = 151
    """ATK up (calculated as passive). A value of 0.12 means ATK +12%."""
    DEF_PASSIVE = 152
    """DEF up (calculated as passive). A value of 0.12 means DEF +12%."""
    CRT_RATE_PASSIVE = 153
    """Critical rate up (calculated as passive). A value of 0.12 means CRT +12%."""
    CRT_DAMAGE_PASSIVE = 154
    """Critical damage up (calculated as passive). A value of 0.12 means CRT DMG +12%."""
    SKILL_DAMAGE_PASSIVE = 155
    """Skill damage up (calculated as passive). A value of 0.12 means SDMG +12%."""
    ASPD_PASSIVE = 156
    """Attack speed up (calculated as passive). A value of 0.12 means ASPD +12%."""
    FS_DAMAGE_PASSIVE = 157
    """Force strike damage up (calculated as passive). A value of 0.12 means FS DMG +12%."""
    # endregion

    # region Infliction probability
    INFLICT_PROB_POISON = 161
    """
    Poison infliction probability up.
    A value of 0.12 means that the probability of inflicting posion is boosted by 12%.
    """
    INFLICT_PROB_BURN = 162
    """
    Burn infliction probability up.
    A value of 0.12 means that the probability of inflicting burn is boosted by 12%.
    """
    INFLICT_PROB_FREEZE = 163
    """
    Freeze infliction probability up.
    A value of 0.12 means that the probability of inflicting freeze is boosted by 12%.
    """
    INFLICT_PROB_PARALYZE = 164
    """
    Paralyze infliction probability up.
    A value of 0.12 means that the probability of inflicting paralyze is boosted by 12%.
    """
    INFLICT_PROB_BLIND = 165
    """
    Blind infliction probability up.
    A value of 0.12 means that the probability of inflicting blind is boosted by 12%.
    """
    INFLICT_PROB_STUN = 166
    """
    Stun infliction probability up.
    A value of 0.12 means that the probability of inflicting posion is boosted by 12%.
    """
    INFLICT_PROB_CURSE = 167
    """
    Curse infliction probability up.
    A value of 0.12 means that the probability of inflicting curse is boosted by 12%.
    """
    INFLICT_PROB_BOG = 169
    """
    Bog infliction probability up.
    A value of 0.12 means that the probability of inflicting bog is boosted by 12%.
    """
    INFLICT_PROB_SLEEP = 170
    """
    Sleep infliction probability up.
    A value of 0.12 means that the probability of inflicting sleep is boosted by 12%.
    """
    INFLICT_PROB_FROSTBITE = 171
    """
    Frostbite infliction probability up.
    A value of 0.12 means that the probability of inflicting frostbite is boosted by 12%.
    """
    INFLICT_PROB_FLASHBURN = 172
    """
    Flashburn infliction probability up.
    A value of 0.12 means that the probability of inflicting flashburn is boosted by 12%.
    """
    INFLICT_PROB_STORMLASH = 173
    """
    Stormlash infliction probability up.
    A value of 0.12 means that the probability of inflicting stormlash is boosted by 12%.
    """
    INFLICT_PROB_SHADOWBLIGHT = 174
    """
    Shadowblight infliction probability up.
    A value of 0.12 means that the probability of inflicting shadowblight is boosted by 12%.
    """
    INFLICT_PROB_SCORCHREND = 175
    """
    Scorchrend infliction probability up.
    A value of 0.12 means that the probability of inflicting scorchrend is boosted by 12%.
    """
    # endregion

    # region EX
    ATK_EX = 191
    """ATK up (calculated as EX). A value of 0.12 means ATK +12%."""
    # endregion
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
    RP_UP = 301
    """Buff the healing power (in RP). A value of 0.12 means to raise the healing power by 12%."""
    HEAL_INSTANT_RP = 302
    """Heal the target instantly by RP. A value of 0.12 means to heal with 12% RP."""
    HEAL_INSTANT_HP = 303
    """Heal the target instantly by max HP. A value of 0.12 means to heal with 12% max HP."""
    HEAL_OVER_TIME_RP = 304
    """Heal the target over time by RP. A value of 0.12 means to heal over time with 12% RP."""
    HEAL_OVER_TIME_HP = 305
    """Heal the target over time by max HP. A value of 0.12 means to heal over time with 12% max HP."""
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
    RESISTANCE_FLAME_BUFF = 411
    """
    Flame resistance up (counter as buff).
    A value of 0.12 means that the user reduces flame damage taken by 12%.
    """
    RESISTANCE_WATER_BUFF = 412
    """
    Water resistance up (counter as buff).
    A value of 0.12 means that the user reduces water damage taken by 12%.
    """
    RESISTANCE_WIND_BUFF = 413
    """
    Wind resistance up (counter as buff).
    A value of 0.12 means that the user reduces wind damage taken by 12%.
    """
    RESISTANCE_LIGHT_BUFF = 414
    """
    Light resistance up (counter as buff).
    A value of 0.12 means that the user reduces light damage taken by 12%.
    """
    RESISTANCE_SHADOW_BUFF = 415
    """
    Shadow resistance up (counter as buff).
    A value of 0.12 means that the user reduces shadow damage taken by 12%.
    """
    RESISTANCE_FLAME_PASSIVE = 416
    """
    Flame resistance up (counter as passive).
    A value of 0.12 means that the user reduces flame damage taken by 12%.
    """
    RESISTANCE_WATER_PASSIVE = 417
    """
    Water resistance up (counter as passive).
    A value of 0.12 means that the user reduces water damage taken by 12%.
    """
    RESISTANCE_WIND_PASSIVE = 418
    """
    Wind resistance up (counter as passive).
    A value of 0.12 means that the user reduces wind damage taken by 12%.
    """
    RESISTANCE_LIGHT_PASSIVE = 419
    """
    Light resistance up (counter as passive).
    A value of 0.12 means that the user reduces light damage taken by 12%.
    """
    RESISTANCE_SHADOW_PASSIVE = 420
    """
    Shadow resistance up (counter as passive).
    A value of 0.12 means that the user reduces shadow damage taken by 12%.
    """
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

    A value of 0.2 means to increase the gauge consumption by 20%.
    This means that to shapeshift once, 70% of the dragon gauge is required
    (shapeshifting once consume 50% dragon gauge normally).
    """
    DP_RATE = 604
    """Change the rate of the dragon point gain. A value of 0.2 means to increase the dragon point gain by 20%."""
    DRAGON_DAMAGE = 605
    """Increased the damage dealt in the dragon form. A value of 0.12 means damage in dragon +12%."""
    DRAGON_GAUGE_FILL = 606
    """
    Fill the dragon gauge by a certain percentage. A value of 0.12 means to fill 12% of the dragon gauge.
    (Shapeshifting once takes 50% of the dragon gauge)
    """
    # endregion

    # region Punishers
    # region Afflicted
    POISONED_PUNISHER = 701
    BURNED_PUNISHER = 702
    FROZEN_PUNISHER = 703
    PARALYZED_PUNISHER = 704
    BLINDED_PUNISHER = 705
    STUNNED_PUNISHER = 706
    CURSED_PUNISHER = 707
    BOGGED_PUNISHER = 709
    SLEPT_PUNISHER = 710
    FROSTBITTEN_PUNISHER = 711
    FLASHBURNED_PUNISHER = 712
    STORMLASHED_PUNISHER = 713
    SHADOWBLIGHTED_PUNISHER = 714
    SCORCHRENT_PUNISHER = 715
    AFFLICTED_PUNISHER = 729
    # endregion

    # region Status
    DEF_DOWN_PUNISHER = 740
    ATK_OR_DEF_DOWN_PUNISHER = 741
    OD_STATE_PUNISHER = 742
    BK_STATE_PUNISHER = 743
    # endregion
    # endregion

    # region Miscellaneous
    # region Special Sentinel
    AFFLICTION = 901
    """The buff is an affliction. Value does not have any meaning."""
    MARK = 902
    """The buff is a mark. Value does not have any meanings. This is used by Nobunaga only as of 2020/12/10."""
    DISPEL = 903
    """Dispels a buff. Value does not have any meaning."""
    # endregion

    # region Miscellaneous
    PLAYER_EXP = 990
    """Raises the player EXP gain upon clearing a quest. A value of 0.12 to raise the player EXP gain by 12%."""
    ENERGY_LEVEL = 991
    """
    Raise the user's energy level. A value of 2 means to raise the energy level by 2.

    Note that the max of the energy level is 5. Upon reaching the max level, the user is energized.
    The power of the next attacking or recovery skill will have either an 50% passive skill damage buff
    or 50% recovery potency buff.
    """
    INSPIRE_LEVEL = 992
    """
    Inspire the user. A value of 2 means to raise the inspiration level by 2.

    Note that the max of the inspire level is 5. Upon reaching the max level, the user is inspired.
    The next attacking skill is guaranteed to be critical for every hit, if the user is inspired.
    """

    # endregion
    # endregion

    @property
    def is_value_percentage(self) -> bool:
        """Check if the value of the buff parameter is percentage."""
        return self.parameter_unit == BuffValueUnit.PERCENTAGE

    @property
    def is_duration_count_meaningless(self) -> bool:
        """Check if duration count (if available) for the buff parameter is meaningless."""
        return self in (BuffParameter.INSPIRE_LEVEL, BuffParameter.ENERGY_LEVEL)

    @property
    def parameter_unit(self) -> BuffValueUnit:
        """Get the unit of the parameter value."""
        return _PARAM_UNIT[self]

    @property
    def translation_id(self) -> str:
        return f"ENUM_BUFF_{self.name}"

    @staticmethod
    def get_all_translatable_members() -> list["BuffParameter"]:
        return list(BuffParameter)


_PARAM_UNIT: dict[BuffParameter, BuffValueUnit] = {
    BuffParameter.ATK_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.DEF_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.CRT_RATE_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.CRT_DAMAGE_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.SKILL_DAMAGE_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.ASPD_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.FS_DAMAGE_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.FS_SPD: BuffValueUnit.PERCENTAGE,
    BuffParameter.OD_GAUGE_DAMAGE: BuffValueUnit.PERCENTAGE,
    BuffParameter.AUTO_DAMAGE: BuffValueUnit.PERCENTAGE,
    BuffParameter.TARGETED_BUFF_TIME: BuffValueUnit.PERCENTAGE,
    BuffParameter.COMBO_TIME: BuffValueUnit.SECONDS,
    BuffParameter.FLAME_ELEM_DMG_UP: BuffValueUnit.PERCENTAGE,
    BuffParameter.WATER_ELEM_DMG_UP: BuffValueUnit.PERCENTAGE,
    BuffParameter.WIND_ELEM_DMG_UP: BuffValueUnit.PERCENTAGE,
    BuffParameter.LIGHT_ELEM_DMG_UP: BuffValueUnit.PERCENTAGE,
    BuffParameter.SHADOW_ELEM_DMG_UP: BuffValueUnit.PERCENTAGE,
    BuffParameter.ATK_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.DEF_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.CRT_RATE_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.CRT_DAMAGE_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.SKILL_DAMAGE_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.ASPD_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.FS_DAMAGE_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_POISON: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_BURN: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_FREEZE: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_PARALYZE: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_BLIND: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_STUN: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_CURSE: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_BOG: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_SLEEP: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_FROSTBITE: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_FLASHBURN: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_STORMLASH: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_SHADOWBLIGHT: BuffValueUnit.PERCENTAGE,
    BuffParameter.INFLICT_PROB_SCORCHREND: BuffValueUnit.PERCENTAGE,
    BuffParameter.ATK_EX: BuffValueUnit.PERCENTAGE,
    BuffParameter.SP_RATE: BuffValueUnit.PERCENTAGE,
    BuffParameter.SP_GAIN: BuffValueUnit.SKILL_POINT,
    BuffParameter.SP_CHARGE_PCT_S1: BuffValueUnit.PERCENTAGE,
    BuffParameter.SP_CHARGE_PCT_S2: BuffValueUnit.PERCENTAGE,
    BuffParameter.SP_CHARGE_PCT_S3: BuffValueUnit.PERCENTAGE,
    BuffParameter.SP_CHARGE_PCT_S4: BuffValueUnit.PERCENTAGE,
    BuffParameter.SP_CHARGE_PCT_USED: BuffValueUnit.PERCENTAGE,
    BuffParameter.RP_UP: BuffValueUnit.PERCENTAGE,
    BuffParameter.HEAL_INSTANT_RP: BuffValueUnit.PERCENTAGE,
    BuffParameter.HEAL_INSTANT_HP: BuffValueUnit.PERCENTAGE,
    BuffParameter.HEAL_OVER_TIME_RP: BuffValueUnit.PERCENTAGE,
    BuffParameter.HEAL_OVER_TIME_HP: BuffValueUnit.PERCENTAGE,
    BuffParameter.SHIELD_SINGLE_DMG: BuffValueUnit.PERCENTAGE,
    BuffParameter.SHIELD_LIFE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_FLAME_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_WATER_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_WIND_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_LIGHT_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_SHADOW_BUFF: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_FLAME_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_WATER_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_WIND_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_LIGHT_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_SHADOW_PASSIVE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_POISON: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_BURN: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_FREEZE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_PARALYZE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_BLIND: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_STUN: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_CURSE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_BOG: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_SLEEP: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_FROSTBITE: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_FLASHBURN: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_STORMLASH: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_SHADOWBLIGHT: BuffValueUnit.PERCENTAGE,
    BuffParameter.RESISTANCE_SCORCHREND: BuffValueUnit.PERCENTAGE,
    BuffParameter.HP_FIX_BY_MAX: BuffValueUnit.PERCENTAGE,
    BuffParameter.HP_DECREASE_BY_MAX: BuffValueUnit.PERCENTAGE,
    BuffParameter.HP_RAISE_BY_MAX: BuffValueUnit.PERCENTAGE,
    BuffParameter.DRAGON_TIME: BuffValueUnit.PERCENTAGE,
    BuffParameter.DRAGON_TIME_FINAL: BuffValueUnit.PERCENTAGE,
    BuffParameter.DP_CONSUMPTION: BuffValueUnit.PERCENTAGE,
    BuffParameter.DP_RATE: BuffValueUnit.PERCENTAGE,
    BuffParameter.DRAGON_DAMAGE: BuffValueUnit.PERCENTAGE,
    BuffParameter.DRAGON_GAUGE_FILL: BuffValueUnit.PERCENTAGE,
    BuffParameter.POISONED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.BURNED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.FROZEN_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.PARALYZED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.BLINDED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.STUNNED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.CURSED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.BOGGED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.SLEPT_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.FROSTBITTEN_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.FLASHBURNED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.STORMLASHED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.SHADOWBLIGHTED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.SCORCHRENT_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.AFFLICTED_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.DEF_DOWN_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.ATK_OR_DEF_DOWN_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.OD_STATE_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.BK_STATE_PUNISHER: BuffValueUnit.PERCENTAGE,
    BuffParameter.AFFLICTION: BuffValueUnit.NONE,
    BuffParameter.MARK: BuffValueUnit.NONE,
    BuffParameter.DISPEL: BuffValueUnit.NONE,
    BuffParameter.PLAYER_EXP: BuffValueUnit.PERCENTAGE,
    BuffParameter.ENERGY_LEVEL: BuffValueUnit.LEVEL,
    BuffParameter.INSPIRE_LEVEL: BuffValueUnit.LEVEL,
}
