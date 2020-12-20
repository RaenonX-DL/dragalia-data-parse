import time

from dlparse.enums import cond_afflictions
from dlparse.export import export_atk_skill_as_csv, export_enums_json, export_sup_skill_as_csv
from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET, PATH_LOCAL_DIR_MASTER_ASSET

_start = time.time()

_asset_manager: AssetManager = AssetManager(
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET
)


def export_atk():
    export_atk_skill_as_csv("exported/skill_atk.csv", asset_manager=_asset_manager)
    print(export_atk_skill_as_csv)


def export_sup():
    export_sup_skill_as_csv("exported/skill_sup.csv", asset_manager=_asset_manager)
    print(export_sup_skill_as_csv)


def export_enums():
    export_enums_json(_asset_manager, cond_afflictions, "exported/enums.json")


def main():
    export_enums()
    print(f"{time.time() - _start:.3f} secs")


if __name__ == '__main__':
    main()
