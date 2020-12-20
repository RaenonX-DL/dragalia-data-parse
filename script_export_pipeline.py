import argparse
import os
from configparser import ConfigParser

from dlparse.enums import cond_afflictions
from dlparse.export import export_enums_json
from dlparse.mono.manager import AssetManager
from dlparse.utils import time_exec


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
    def _export_enums(self):
        export_enums_json(self._asset_manager, cond_afflictions, os.path.join(self._dir_export, "enums.json"))

    @time_exec(title="Total exporting time")
    def export(self):
        """Export the parsed assets."""
        self._export_enums()


# region Parser
parser = argparse.ArgumentParser(description="Process the assets and export it as website resources.")
parser.add_argument("--config", type=str, help="Location of the config file.",
                    dest="config_path", default="export.ini")
# endregion


if __name__ == '__main__':
    FileExporter(parser.parse_args().config_path).export()
