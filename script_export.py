from dlparse.export import export_atk_skill_as_csv, export_sup_skill_as_csv
from dlparse.mono.manager import AssetManager
from tests.static import PATH_DIR_MASTER_ASSET, PATH_ROOT_ASSET_PLAYER_ACTION

_asset_manager: AssetManager = AssetManager(PATH_ROOT_ASSET_PLAYER_ACTION, PATH_DIR_MASTER_ASSET)


def export_atk():
    export_atk_skill_as_csv("exported/skill_atk.csv", asset_manager=_asset_manager)


def export_sup():
    export_sup_skill_as_csv("exported/skill_sup.csv", asset_manager=_asset_manager)


if __name__ == '__main__':
    export_sup()
