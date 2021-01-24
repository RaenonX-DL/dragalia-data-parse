"""Implementations of getting the related image of an enum."""
from typing import Optional, Union

from .buff_parameter import BuffParameter
from .condition import Condition
from .element import Element

__all__ = ("get_image_path",)

TransformableEnums = Union[Element, Condition, BuffParameter]

path_dict: dict[TransformableEnums, str] = {
    Element.FLAME: "/icon/element/m/Icon_02_Flame.png",
    Element.WATER: "/icon/element/m/Icon_02_Water.png",
    Element.WIND: "/icon/element/m/Icon_02_Wind.png",
    Element.LIGHT: "/icon/element/m/Icon_02_Light.png",
    Element.SHADOW: "/icon/element/m/Icon_02_Dark.png",
    Condition.TARGET_POISONED: "/icon/status/Icon_Status_01_01.png",
    Condition.TARGET_BURNED: "/icon/status/Icon_Status_01_02.png",
    Condition.TARGET_FROZEN: "/icon/status/Icon_Status_01_03.png",
    Condition.TARGET_PARALYZED: "/icon/status/Icon_Status_01_04.png",
    Condition.TARGET_BLINDED: "/icon/status/Icon_Status_01_05.png",
    Condition.TARGET_STUNNED: "/icon/status/Icon_Status_01_06.png",
    Condition.TARGET_CURSED: "/icon/status/Icon_Status_01_07.png",
    Condition.TARGET_BOGGED: "/icon/status/Icon_Status_01_09.png",
    Condition.TARGET_SLEPT: "/icon/status/Icon_Status_01_10.png",
    Condition.TARGET_FROSTBITTEN: "/icon/status/Icon_Status_01_11.png",
    Condition.TARGET_FLASHBURNED: "/icon/status/Icon_Status_01_12.png",
    Condition.TARGET_STORMLASHED: "/icon/status/Icon_Status_01_13.png",
    Condition.TARGET_SHADOWBLIGHTED: "/icon/status/Icon_Status_01_14.png",
    Condition.TARGET_SCORCHRENT: "/icon/status/Icon_Status_01_15.png",
    Condition.TARGET_FLAME: "/icon/element/m/Icon_02_Flame.png",
    Condition.TARGET_WATER: "/icon/element/m/Icon_02_Water.png",
    Condition.TARGET_WIND: "/icon/element/m/Icon_02_Wind.png",
    Condition.TARGET_LIGHT: "/icon/element/m/Icon_02_Light.png",
    Condition.TARGET_SHADOW: "/icon/element/m/Icon_02_Dark.png",
    BuffParameter.ATK_BUFF: "/icon/ability/l/Icon_Ability_1020002.png",
    BuffParameter.DEF_BUFF: "/icon/ability/l/Icon_Ability_1020003.png",
    BuffParameter.CRT_RATE_BUFF: "/icon/ability/l/Icon_Ability_1020010.png",
    BuffParameter.CRT_DAMAGE_BUFF: "/icon/ability/l/Icon_Ability_1020011.png",
    BuffParameter.SKILL_DAMAGE_BUFF: "/icon/ability/l/Icon_Ability_1010002.png",
    BuffParameter.ASPD_BUFF: "/icon/ability/l/Icon_Ability_1020014.png",
    BuffParameter.FS_DAMAGE_BUFF: "/icon/ability/l/Icon_Ability_1010001.png",
    BuffParameter.FS_SPD: "/icon/ability/l/Icon_Ability_1010092.png",
    BuffParameter.OD_GAUGE_DAMAGE: "/icon/ability/l/Icon_Ability_1020013.png",
    BuffParameter.AUTO_DAMAGE: "/icon/ability/l/Icon_Ability_1010045.png",
    BuffParameter.TARGETED_BUFF_TIME: "/icon/ability/l/Icon_Ability_1010006.png",
    BuffParameter.COMBO_TIME: "/icon/ability/l/Icon_Ability_1020036.png",
    BuffParameter.FLAME_ELEM_DMG_UP: "/icon/ability/l/Icon_Ability_1090001.png",
    BuffParameter.WATER_ELEM_DMG_UP: "/icon/ability/l/Icon_Ability_1090002.png",
    BuffParameter.WIND_ELEM_DMG_UP: "/icon/ability/l/Icon_Ability_1090003.png",
    BuffParameter.LIGHT_ELEM_DMG_UP: "/icon/ability/l/Icon_Ability_1090004.png",
    BuffParameter.SHADOW_ELEM_DMG_UP: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.ATK_PASSIVE: "/icon/ability/l/Icon_Ability_1020002.png",
    BuffParameter.DEF_PASSIVE: "/icon/ability/l/Icon_Ability_1020003.png",
    BuffParameter.CRT_RATE_PASSIVE: "/icon/ability/l/Icon_Ability_1020010.png",
    BuffParameter.CRT_DAMAGE_PASSIVE: "/icon/ability/l/Icon_Ability_1020011.png",
    BuffParameter.SKILL_DAMAGE_PASSIVE: "/icon/ability/l/Icon_Ability_1010002.png",
    BuffParameter.ASPD_PASSIVE: "/icon/ability/l/Icon_Ability_1020014.png",
    BuffParameter.FS_DAMAGE_PASSIVE: "/icon/ability/l/Icon_Ability_1010001.png",
    BuffParameter.INFLICT_PROB_POISON: "/icon/ability/l/Icon_Ability_1040001.png",
    BuffParameter.INFLICT_PROB_BURN: "/icon/ability/l/Icon_Ability_1040002.png",
    BuffParameter.INFLICT_PROB_FREEZE: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.INFLICT_PROB_PARALYZE: "/icon/ability/l/Icon_Ability_1040004.png",
    BuffParameter.INFLICT_PROB_BLIND: "/icon/ability/l/Icon_Ability_1040005.png",
    BuffParameter.INFLICT_PROB_STUN: "/icon/ability/l/Icon_Ability_1040006.png",
    BuffParameter.INFLICT_PROB_CURSE: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.INFLICT_PROB_BOG: "/icon/ability/l/Icon_Ability_1040009.png",
    BuffParameter.INFLICT_PROB_SLEEP: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.INFLICT_PROB_FROSTBITE: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.INFLICT_PROB_FLASHBURN: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.INFLICT_PROB_STORMLASH: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.INFLICT_PROB_SHADOWBLIGHT: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.INFLICT_PROB_SCORCHREND: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.ATK_EX: "/icon/ability/l/Icon_Ability_1020002.png",
    BuffParameter.SP_RATE: "/icon/ability/l/Icon_Ability_1020004.png",
    BuffParameter.SP_GAIN: "/icon/ability/l/Icon_Ability_1010007.png",
    BuffParameter.SP_CHARGE_PCT_S1: "/icon/ability/l/Icon_Ability_1010007.png",
    BuffParameter.SP_CHARGE_PCT_S2: "/icon/ability/l/Icon_Ability_1010007.png",
    BuffParameter.SP_CHARGE_PCT_S3: "/icon/ability/l/Icon_Ability_1010007.png",
    BuffParameter.SP_CHARGE_PCT_S4: "/icon/ability/l/Icon_Ability_1010007.png",
    BuffParameter.SP_CHARGE_PCT_USED: "/icon/ability/l/Icon_Ability_1010007.png",
    BuffParameter.HEAL_RP: "/icon/ability/l/Icon_Ability_1020009.png",
    BuffParameter.HEAL_MAX_HP: "/icon/ability/l/Icon_Ability_1020009.png",
    BuffParameter.SHIELD_SINGLE_DMG: "/icon/ability/l/Icon_Ability_1020022.png",
    BuffParameter.SHIELD_LIFE: "/icon/ability/l/Icon_Ability_1020037.png",
    BuffParameter.RESISTANCE_FLAME: "/icon/ability/l/Icon_Ability_1080001.png",
    BuffParameter.RESISTANCE_WATER: "/icon/ability/l/Icon_Ability_1080002.png",
    BuffParameter.RESISTANCE_WIND: "/icon/ability/l/Icon_Ability_1080003.png",
    BuffParameter.RESISTANCE_LIGHT: "/icon/ability/l/Icon_Ability_1080004.png",
    BuffParameter.RESISTANCE_SHADOW: "/icon/ability/l/Icon_Ability_1080005.png",
    BuffParameter.RESISTANCE_POISON: "/icon/ability/l/Icon_Ability_1030001.png",
    BuffParameter.RESISTANCE_BURN: "/icon/ability/l/Icon_Ability_1030002.png",
    BuffParameter.RESISTANCE_FREEZE: "/icon/ability/l/Icon_Ability_1030003.png",
    BuffParameter.RESISTANCE_PARALYZE: "/icon/ability/l/Icon_Ability_1030004.png",
    BuffParameter.RESISTANCE_BLIND: "/icon/ability/l/Icon_Ability_1030005.png",
    BuffParameter.RESISTANCE_STUN: "/icon/ability/l/Icon_Ability_1030006.png",
    BuffParameter.RESISTANCE_CURSE: "/icon/ability/l/Icon_Ability_1030007.png",
    BuffParameter.RESISTANCE_BOG: "/icon/ability/l/Icon_Ability_1030009.png",
    BuffParameter.RESISTANCE_SLEEP: "/icon/ability/l/Icon_Ability_1030010.png",
    BuffParameter.RESISTANCE_FROSTBITE: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.RESISTANCE_FLASHBURN: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.RESISTANCE_STORMLASH: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.RESISTANCE_SHADOWBLIGHT: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.RESISTANCE_SCORCHREND: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.HP_FIX_BY_MAX: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.HP_DECREASE_BY_MAX: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.HP_RAISE_BY_MAX: "/icon/ability/l/Icon_Ability_1020001.png",
    BuffParameter.DRAGON_TIME: "/icon/ability/l/Icon_Ability_1010003.png",
    BuffParameter.DRAGON_TIME_FINAL: "/icon/ability/l/Icon_Ability_1010003.png",
    BuffParameter.DP_CONSUMPTION: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.DP_RATE: "/icon/ability/l/Icon_Ability_1020005.png",
    # Borrowed from Gala Euden (10150403) EX
    BuffParameter.DRAGON_DAMAGE: "/icon/ability/l/Icon_Ability_1020032.png",
    BuffParameter.DRAGON_GAUGE_FILL: "/icon/ability/l/Icon_Ability_1010008.png",
    BuffParameter.POISONED_PUNISHER: "/icon/ability/l/Icon_Ability_1070001.png",
    BuffParameter.BURNED_PUNISHER: "/icon/ability/l/Icon_Ability_1070002.png",
    BuffParameter.FROZEN_PUNISHER: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.PARALYZED_PUNISHER: "/icon/ability/l/Icon_Ability_1070004.png",
    BuffParameter.BLINDED_PUNISHER: "/icon/ability/l/Icon_Ability_1070005.png",
    BuffParameter.STUNNED_PUNISHER: "/icon/ability/l/Icon_Ability_1070006.png",
    BuffParameter.CURSED_PUNISHER: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.BOGGED_PUNISHER: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.SLEPT_PUNISHER: "/icon/ability/l/Icon_Ability_1070010.png",
    BuffParameter.FROSTBITTEN_PUNISHER: "/icon/ability/l/Icon_Ability_1070013.png",
    BuffParameter.FLASHBURNED_PUNISHER: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.STORMLASHED_PUNISHER: "/icon/ability/l/Icon_Ability_1070018.png",
    BuffParameter.SHADOWBLIGHTED_PUNISHER: "/icon/ability/l/Icon_Ability_1070017.png",
    BuffParameter.SCORCHRENT_PUNISHER: "/icon/ability/l/Icon_Ability_1070019.png",
    BuffParameter.AFFLICTED_PUNISHER: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.DEF_DOWN_PUNISHER: "/icon/ability/l/Icon_Ability_1070015.png",
    BuffParameter.ATK_OR_DEF_DOWN_PUNISHER: "/icon/ability/l/Icon_Ability_1070016.png",
    BuffParameter.OD_STATE_PUNISHER: "/icon/ability/l/Icon_Ability_1010010.png",
    BuffParameter.BK_STATE_PUNISHER: "/icon/ability/l/Icon_Ability_1010009.png",
    BuffParameter.AFFLICTION: None,  # No suitable icon, ``None`` to display the text
    BuffParameter.MARK: None,  # No suitable icon, ``None`` to display the text
    # Borrowed from Nobunaga (10250103) passive
    BuffParameter.DISPEL: "/icon/ability/l/Icon_Ability_1010031.png",
    BuffParameter.PLAYER_EXP: "/icon/ability/l/Icon_Ability_1010003.png",
    BuffParameter.ENERGY_LEVEL: "/icon/ability/l/Icon_Ability_1010012.png",
    BuffParameter.INSPIRE_LEVEL: "/icon/ability/l/Icon_Ability_1010055.png"
}


def get_image_path(enum: TransformableEnums) -> Optional[str]:
    """
    Get the image path of ``enum``. Returns ``None`` if not found.

    The root directory of the path is ``assets/_gluonresources/resources/image``.

    The returned path will start with a slash "/".
    """
    return path_dict.get(enum)
