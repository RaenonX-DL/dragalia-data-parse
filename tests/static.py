import os

__all__ = ("PATH_DIR_MASTER_ASSET", "PATH_DIR_CUSTOM_ASSET", "PATH_ROOT_ASSET_PLAYER_ACTION")

PATH_ROOT_DATA = ".data"
PATH_ROOT_ASSET = os.path.join(PATH_ROOT_DATA, "media", "assets", "_gluonresources", "resources")

PATH_ROOT_ASSET_PLAYER_ACTION = os.path.join(PATH_ROOT_ASSET, "actions", "playeraction")
PATH_DIR_MASTER_ASSET = os.path.join(PATH_ROOT_ASSET, "master")
PATH_DIR_CUSTOM_ASSET = os.path.join(PATH_ROOT_DATA, "custom")
