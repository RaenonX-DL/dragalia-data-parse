"""Function to export the condition enums."""
import json
import os
from typing import TYPE_CHECKING

from dlparse.enums import ColorTheme, Condition, get_image_path
from dlparse.export.entry import ConditionEnumEntry, TextEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("export_condition_entries", "export_condition_as_json", "condition_theme")

# Hard-coded the data to be exported to avoid unnecessary implementations,
# because this almost never change.
# ---------------------------------
# Conditions that are not defined in ``condition_theme`` should use ``default_theme``.

default_theme = ColorTheme.SECONDARY

# region Themes (by category)
theme_target_affliction = ColorTheme.INFO
theme_target_element = ColorTheme.PRIMARY
theme_target_state = ColorTheme.DANGER
theme_target_abnormal = ColorTheme.INFO
theme_self_hp = ColorTheme.WARNING
theme_self_combo = ColorTheme.SUCCESS
theme_skill_bullet_hit = ColorTheme.SUCCESS
theme_teammate_coverage = ColorTheme.SUCCESS
theme_bullets_on_map = ColorTheme.SUCCESS
theme_addl_input = ColorTheme.SUCCESS
# endregion

# region Themes (actual definition)
condition_theme = {
    Condition.TARGET_POISONED: theme_target_affliction,
    Condition.TARGET_BURNED: theme_target_affliction,
    Condition.TARGET_FROZEN: theme_target_affliction,
    Condition.TARGET_PARALYZED: theme_target_affliction,
    Condition.TARGET_BLINDED: theme_target_affliction,
    Condition.TARGET_STUNNED: theme_target_affliction,
    Condition.TARGET_CURSED: theme_target_affliction,
    Condition.TARGET_BOGGED: theme_target_affliction,
    Condition.TARGET_SLEPT: theme_target_affliction,
    Condition.TARGET_FROSTBITTEN: theme_target_affliction,
    Condition.TARGET_FLASHBURNED: theme_target_affliction,
    Condition.TARGET_STORMLASHED: theme_target_affliction,
    Condition.TARGET_SHADOWBLIGHTED: theme_target_affliction,
    Condition.TARGET_SCORCHRENT: theme_target_affliction,
    Condition.TARGET_ELEM_FLAME: theme_target_element,
    Condition.TARGET_ELEM_WATER: theme_target_element,
    Condition.TARGET_ELEM_WIND: theme_target_element,
    Condition.TARGET_ELEM_LIGHT: theme_target_element,
    Condition.TARGET_ELEM_SHADOW: theme_target_element,
    Condition.TARGET_OD_STATE: theme_target_state,
    Condition.TARGET_BK_STATE: theme_target_state,
    Condition.TARGET_AFFLICTED: theme_target_abnormal,
    Condition.TARGET_DEF_DOWN: theme_target_abnormal,
    Condition.TARGET_BUFFED: theme_target_abnormal,
    Condition.TARGET_DEBUFFED: theme_target_abnormal,
    Condition.SELF_HP_1: theme_self_hp,
    Condition.SELF_HP_EQ_10: theme_self_hp,
    Condition.SELF_HP_EQ_20: theme_self_hp,
    Condition.SELF_HP_EQ_30: theme_self_hp,
    Condition.SELF_HP_EQ_50: theme_self_hp,
    Condition.SELF_HP_EQ_70: theme_self_hp,
    Condition.SELF_HP_FULL: theme_self_hp,
    Condition.SELF_HP_LT_40: theme_self_hp,
    Condition.SELF_HP_LT_30: theme_self_hp,
    Condition.SELF_HP_GT_30: theme_self_hp,
    Condition.SELF_HP_GTE_40: theme_self_hp,
    Condition.SELF_HP_GTE_50: theme_self_hp,
    Condition.SELF_HP_GTE_60: theme_self_hp,
    Condition.SELF_HP_GTE_85: theme_self_hp,
    Condition.COMBO_0: theme_self_combo,
    Condition.COMBO_5: theme_self_combo,
    Condition.COMBO_10: theme_self_combo,
    Condition.COMBO_15: theme_self_combo,
    Condition.COMBO_20: theme_self_combo,
    Condition.COMBO_25: theme_self_combo,
    Condition.COMBO_30: theme_self_combo,
    Condition.BULLET_HIT_1: theme_skill_bullet_hit,
    Condition.BULLET_HIT_2: theme_skill_bullet_hit,
    Condition.BULLET_HIT_3: theme_skill_bullet_hit,
    Condition.BULLET_HIT_4: theme_skill_bullet_hit,
    Condition.BULLET_HIT_5: theme_skill_bullet_hit,
    Condition.BULLET_HIT_6: theme_skill_bullet_hit,
    Condition.BULLET_HIT_7: theme_skill_bullet_hit,
    Condition.BULLET_HIT_8: theme_skill_bullet_hit,
    Condition.BULLET_HIT_9: theme_skill_bullet_hit,
    Condition.BULLET_HIT_10: theme_skill_bullet_hit,
    Condition.COVER_TEAMMATE_0: theme_teammate_coverage,
    Condition.COVER_TEAMMATE_1: theme_teammate_coverage,
    Condition.COVER_TEAMMATE_2: theme_teammate_coverage,
    Condition.COVER_TEAMMATE_3: theme_teammate_coverage,
    Condition.BULLETS_ON_MAP_0: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_1: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_2: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_3: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_4: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_5: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_6: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_7: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_8: theme_bullets_on_map,
    Condition.BULLETS_ON_MAP_9: theme_bullets_on_map,
    Condition.ADDL_INPUT_0: theme_addl_input,
    Condition.ADDL_INPUT_1: theme_addl_input,
    Condition.ADDL_INPUT_2: theme_addl_input,
    Condition.ADDL_INPUT_3: theme_addl_input,
    Condition.ADDL_INPUT_4: theme_addl_input,
    Condition.ADDL_INPUT_5: theme_addl_input,
    Condition.ADDL_INPUT_6: theme_addl_input,
}


# endregion


def export_condition_entries(asset_manager: "AssetManager") -> dict[int, ConditionEnumEntry]:
    """Export the condition enums as a dict with key as the code and the value as the entry."""
    return {
        condition.value: ConditionEnumEntry(
            enum_name=condition.name, enum_code=condition.value, enum_image_path=get_image_path(condition),
            color_theme=condition_theme.get(condition, default_theme),
            trans=TextEntry(asset_manager.asset_text_website, f"ENUM_COND_{condition.name}")
        )
        for condition in Condition
    }


def export_condition_as_json(asset_manager: "AssetManager", file_path: str):
    """
    Export all condition enums as a json file to ``file_path``.

    Data is hard-coded in the module.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if needed

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        json.dump(
            {key: entry.to_json_entry() for key, entry in export_condition_entries(asset_manager).items()},
            f, ensure_ascii=False
        )