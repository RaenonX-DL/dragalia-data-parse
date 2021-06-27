import argparse
import os
from configparser import ConfigParser
from typing import Sequence, TypeVar

from dlparse.enums import (
    BuffValueUnit, Element, SkillCancelAction, Status, TranslatableEnumMixin, Weapon, cond_afflictions, cond_elements,
)
from dlparse.export import (
    collect_chained_ex_ability_buff_param, collect_ex_ability_buff_param, export_atk_skill_as_json,
    export_chara_info_as_json, export_condition_as_json, export_dragon_info_as_json, export_elem_bonus_as_json,
    export_enums_json, export_ex_abilities_as_json, export_skill_identifiers_as_json,
)
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer
from dlparse.utils import time_exec

T = TypeVar("T", bound=TranslatableEnumMixin)


class FileExporter:
    """Class for the asset exporting procedure."""

    @time_exec(title="Loading time")
    def __init__(self, config_path: str):
        config = ConfigParser()
        config.read(config_path)

        dir_action = config.get("Asset", "Action")
        dir_master = config.get("Asset", "Master")
        dir_chara_motion = config.get("Asset", "CharaMotion")
        dir_dragon_motion = config.get("Asset", "DragonMotion")
        dir_custom = config.get("Asset", "Custom")

        dir_export = config.get("Export", "Dir")

        print(f"Action Asset Path: {dir_action}")
        print(f"Master Asset Path: {dir_master}")
        print(f"Character Motion Asset Path: {dir_chara_motion}")
        print(f"Custom Asset Path: {dir_custom}")
        print()
        print(f"Export directory: {dir_export}")
        print()

        self._asset_manager: AssetManager = AssetManager(
            dir_action, dir_master, dir_chara_motion, dir_dragon_motion,
            custom_asset_dir=dir_custom
        )
        self._transformer_ability: AbilityTransformer = AbilityTransformer(self._asset_manager)
        self._dir_export: str = dir_export

    @time_exec(title="Enums exporting time")
    def _export_enums(self, enums: dict[str, Sequence[T]], name: str):
        export_enums_json(self._asset_manager, enums, os.path.join(self._dir_export, "enums", f"{name}.json"))

    @time_exec(title="Condition enums exporting time")
    def _export_enums_condition(self, name: str):
        export_condition_as_json(self._asset_manager, os.path.join(self._dir_export, "enums", f"{name}.json"))

    @time_exec(title="EX/CEX enums exporting time")
    def _export_enums_ex(self):
        enums_ex = collect_ex_ability_buff_param(self._transformer_ability, self._asset_manager)
        enums_cex = collect_chained_ex_ability_buff_param(self._transformer_ability, self._asset_manager)

        self._export_enums({"exBuffParam": enums_ex, "chainedExBuffParam": enums_cex}, "exParam")

    @time_exec(title="Element bonus exporting time")
    def _export_elem_bonus(self):
        export_elem_bonus_as_json(os.path.join(self._dir_export, "misc", "elementBonus.json"))

    @time_exec(title="Skill identifiers exporting time")
    def _export_skill_identifiers(self, name: str):
        export_skill_identifiers_as_json(self._asset_manager, os.path.join(self._dir_export, "skills", f"{name}.json"))

    @time_exec(title="ATK skill exporting time")
    def _export_atk_skill(self):
        export_atk_skill_as_json(
            os.path.join(self._dir_export, "skills", "attacking.json"), self._asset_manager,
            skip_unparsable=True
        )

    @time_exec(title="EX/CEX ability exporting time")
    def _export_ex_abilities(self):
        export_ex_abilities_as_json(
            os.path.join(self._dir_export, "abilities", "ex.json"), self._asset_manager,
            skip_unparsable=True
        )

    @time_exec(title="Unit info exporting time")
    def _export_unit_info(self):
        export_chara_info_as_json(
            os.path.join(self._dir_export, "info", "chara.json"), self._asset_manager,
            skip_unparsable=True
        )
        export_dragon_info_as_json(
            os.path.join(self._dir_export, "info", "dragon.json"), self._asset_manager,
            skip_unparsable=True
        )

    @time_exec(title="Total exporting time")
    def export(self):
        """Export the parsed assets."""
        # Enums
        self._export_enums({"afflictions": cond_afflictions, "elements": cond_elements}, "conditions")
        self._export_enums_ex()
        self._export_enums({"weapon": Weapon.get_all_translatable_members()}, "weaponType")
        self._export_enums({"elemental": Element.get_all_translatable_members()}, "elements")
        self._export_enums({"unit": BuffValueUnit.get_all_translatable_members()}, "buffParam")
        self._export_enums({"status": Status.get_all_translatable_members()}, "status")
        self._export_enums({"cancel": SkillCancelAction.get_all_translatable_members()}, "skill")
        self._export_enums_condition("allCondition")

        # Skill
        self._export_atk_skill()
        self._export_skill_identifiers("identifiers")

        # Abilties
        self._export_ex_abilities()

        # Unit info
        self._export_unit_info()

        # Misc
        self._export_elem_bonus()


# region Parser
parser = argparse.ArgumentParser(description="Process the assets and export it as website resources.")
parser.add_argument("--config", type=str, help="Location of the config file.",
                    dest="config_path", default="export.ini")
# endregion


if __name__ == '__main__':
    FileExporter(parser.parse_args().config_path).export()
