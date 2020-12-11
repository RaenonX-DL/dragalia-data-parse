from dlparse.export import export_atk_skill_as_csv, export_sup_skill_as_csv
from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET

_asset_manager: AssetManager = AssetManager(PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET)


def export_atk():
    export_atk_skill_as_csv("exported/skill_atk.csv", asset_manager=_asset_manager)
    print(export_atk_skill_as_csv)


def export_sup():
    export_sup_skill_as_csv("exported/skill_sup.csv", asset_manager=_asset_manager)
    print(export_sup_skill_as_csv)


if __name__ == '__main__':
    export_atk()
