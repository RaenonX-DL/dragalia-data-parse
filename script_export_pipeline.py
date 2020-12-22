import argparse
import os
from configparser import ConfigParser
from enum import Enum
from typing import Sequence, TypeVar

from dlparse.enums import cond_afflictions, cond_elements
from dlparse.export import export_atk_skill_as_json, export_elem_bonus_as_json, export_enums_json
from dlparse.mono.manager import AssetManager
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
        dir_custom = config.get("Asset", "Custom")

        dir_export = config.get("Export", "Dir")

        print(f"Action Asset Path: {dir_action}")
        print(f"Master Asset Path: {dir_master}")
        print(f"Custom Asset Path: {dir_custom}")
        print()
        print(f"Export directory: {dir_export}")
        print()

        self._asset_manager: AssetManager = AssetManager(dir_action, dir_master, custom_asset_dir=dir_custom)
        self._dir_export: str = dir_export

    @time_exec(title="Enums exporting time")
    def _export_enums(self, enums: dict[str, Sequence[T]], name: str):
        export_enums_json(self._asset_manager, enums, os.path.join(self._dir_export, "enums", f"{name}.json"))

    @time_exec(title="Element bonus exporting time")
    def _export_elem_bonus(self):
        export_elem_bonus_as_json(os.path.join(self._dir_export, "misc", "elementBonus.json"))

    @time_exec(title="ATK skill exporting time")
    def _export_atk_skill(self):
        export_atk_skill_as_json(
            os.path.join(self._dir_export, "skills", "attacking.json"), self._asset_manager,
            skip_unparsable=False
        )

    @time_exec(title="Total exporting time")
    def export(self):
        """Export the parsed assets."""
        # Enums
        self._export_enums({"afflictions": cond_afflictions, "elements": cond_elements}, "conditions")
        # Misc
        self._export_elem_bonus()
        # Skill
        self._export_atk_skill()


# region Parser
parser = argparse.ArgumentParser(description="Process the assets and export it as website resources.")
parser.add_argument("--config", type=str, help="Location of the config file.",
                    dest="config_path", default="export.ini")
# endregion


if __name__ == '__main__':
    FileExporter(parser.parse_args().config_path).export()
