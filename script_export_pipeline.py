import argparse
import os
from configparser import ConfigParser
from enum import Enum
from typing import Sequence, TypeVar

from dlparse.enums import Element, cond_afflictions, cond_elements
from dlparse.export import (
    collect_chained_ex_ability_buff_param, collect_ex_ability_buff_param, export_atk_skill_as_json,
    export_condition_as_json, export_elem_bonus_as_json, export_enums_json, export_skill_identifiers_as_json,
)
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer
from dlparse.utils import time_exec

T = TypeVar("T", bound=Enum)


class FileExporter:
    """Class for the asset exporting procedure."""

    @time_exec(title="Loading time")
    def __init__(self, config_path: str):
        config = ConfigParser()
        config.read(config_path)

        dir_action = config.get("Asset", "Action")
        dir_master = config.get("Asset", "Master")
        dir_chara_motion = config.get("Asset", "CharaMotion")
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
            dir_action, dir_master, dir_chara_motion,
            custom_asset_dir=dir_custom
        )
        self._transformer_ability: AbilityTransformer = AbilityTransformer(self._asset_manager)
        self._dir_export: str = dir_export

    @time_exec(title="Enums exporting time")
    def _export_enums(self, enums: dict[str, Sequence[T]], name: str, /, prefix: str = "ENUM_"):
        export_enums_json(
            self._asset_manager, enums, os.path.join(self._dir_export, "enums", f"{name}.json"),
            prefix=prefix
        )

    @time_exec(title="Condition enums exporting time")
    def _export_enums_condition(self, name: str):
        export_condition_as_json(self._asset_manager, os.path.join(self._dir_export, "enums", f"{name}.json"))

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

    @time_exec(title="Total exporting time")
    def export(self):
        """Export the parsed assets."""
        # Enums
        self._export_enums({"afflictions": cond_afflictions, "elements": cond_elements}, "conditions")
        self._export_enums(
            {
                "exBuffParam": collect_ex_ability_buff_param(self._transformer_ability, self._asset_manager),
                "chainedExBuffParam": collect_chained_ex_ability_buff_param(
                    self._transformer_ability, self._asset_manager
                )
            },
            "exParam",
            prefix="BUFF_"
        )
        self._export_enums({"elemental": Element.get_all_valid_elements()}, "elements")
        self._export_enums_condition("allCondition")
        # Misc
        self._export_elem_bonus()
        # Skill
        self._export_atk_skill()
        self._export_skill_identifiers("identifiers")


# region Parser
parser = argparse.ArgumentParser(description="Process the assets and export it as website resources.")
parser.add_argument("--config", type=str, help="Location of the config file.",
                    dest="config_path", default="export.ini")
# endregion


if __name__ == '__main__':
    FileExporter(parser.parse_args().config_path).export()
