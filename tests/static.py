import os

__all__ = (
    "PATH_LOCAL_DIR_MASTER_ASSET", "PATH_LOCAL_DIR_CUSTOM_ASSET", "PATH_LOCAL_DIR_ACTION_ASSET",
    "PATH_LOCAL_DIR_CHARA_MOTION_ASSET", "PATH_LOCAL_DIR_DRAGON_MOTION_ASSET",
    "get_remote_dir_action_asset", "get_remote_dir_master_asset",
    "get_remote_dir_chara_motion_asset", "get_remote_dir_dragon_motion_asset"
)

PATH_LOCAL_ROOT_DATA = ".data"
PATH_LOCAL_ROOT_ASSET = os.path.join(PATH_LOCAL_ROOT_DATA, "media", "assets", "_gluonresources", "resources")

PATH_LOCAL_DIR_ACTION_ASSET = os.path.join(PATH_LOCAL_ROOT_ASSET, "actions")
PATH_LOCAL_DIR_MASTER_ASSET = os.path.join(PATH_LOCAL_ROOT_ASSET, "master")
PATH_LOCAL_DIR_CHARA_MOTION_ASSET = os.path.join(PATH_LOCAL_ROOT_ASSET, "characters", "motion")
PATH_LOCAL_DIR_DRAGON_MOTION_ASSET = os.path.join(PATH_LOCAL_ROOT_ASSET, "dragon", "motion")
PATH_LOCAL_DIR_CUSTOM_ASSET = os.path.join(PATH_LOCAL_ROOT_DATA, "custom")

PATH_REMOTE_GH = "https://raw.githubusercontent.com/RaenonX-DL/dragalia-data-depot/"

REMOTE_VERSION_TAG = "2021.04.15-tKNhlutrX4LPXPUk"


def get_remote_dir_action_asset(version_tag: str = None) -> str:
    """
    Get the remote action asset directory.

    The format of ``version_tag`` should be ``YYYY.MM.DD-VERSION_CODE``.

    The return does **NOT** end with a slash.
    """
    if not version_tag:
        version_tag = REMOTE_VERSION_TAG

    return f"{PATH_REMOTE_GH}{version_tag}/assets/_gluonresources/resources/actions"


def get_remote_dir_master_asset(version_tag: str = None) -> str:
    """
    Get the remote master asset directory.

    The format of ``version_tag`` should be ``YYYY.MM.DD-VERSION_CODE``.

    The return does **NOT** end with a slash.
    """
    if not version_tag:
        version_tag = REMOTE_VERSION_TAG

    return f"{PATH_REMOTE_GH}{version_tag}/assets/_gluonresources/resources/master"


def get_remote_dir_chara_motion_asset(version_tag: str = None) -> str:
    """
    Get the remote character motion asset directory.

    The format of ``version_tag`` should be ``YYYY.MM.DD-VERSION_CODE``.

    The return does **NOT** end with a slash.
    """
    if not version_tag:
        version_tag = REMOTE_VERSION_TAG

    return f"{PATH_REMOTE_GH}{version_tag}/assets/_gluonresources/resources/characters/motion"


def get_remote_dir_dragon_motion_asset(version_tag: str = None) -> str:
    """
    Get the remote dragon motion asset directory.

    The format of ``version_tag`` should be ``YYYY.MM.DD-VERSION_CODE``.

    The return does **NOT** end with a slash.
    """
    if not version_tag:
        version_tag = REMOTE_VERSION_TAG

    return f"{PATH_REMOTE_GH}{version_tag}/assets/_gluonresources/resources/dragon/motion"
