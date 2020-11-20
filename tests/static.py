import os

__all__ = ("PATH_MASTER_ASSET_DIR", "PATH_PLAYER_ACTION_ASSET_ROOT")


PATH_ASSET_ROOT = os.path.join(".data", "media", "assets", "_gluonresources", "resources")

PATH_PLAYER_ACTION_ASSET_ROOT = os.path.join(PATH_ASSET_ROOT, "actions", "playeraction")
PATH_MASTER_ASSET_DIR = os.path.join(PATH_ASSET_ROOT, "master")
