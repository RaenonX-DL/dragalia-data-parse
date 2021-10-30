import os

__all__ = (
    "PATH_LOCAL_ROOT_RESOURCES", "PATH_LOCAL_DIR_CUSTOM_ASSET",
    "get_remote_dir_root_resources", "get_remote_dir_root"
)

PATH_LOCAL_ROOT_DATA = ".data"
PATH_LOCAL_ROOT_RESOURCES = os.path.join(PATH_LOCAL_ROOT_DATA, "media", "assets", "_gluonresources", "resources")

PATH_LOCAL_DIR_CUSTOM_ASSET = os.path.join(PATH_LOCAL_ROOT_DATA, "custom")

PATH_REMOTE_GH = "https://raw.githubusercontent.com/RaenonX-DL/dragalia-data-depot/"

REMOTE_VERSION_TAG = "2021.10.28-P5vciqNVlQONmeQr"


def get_remote_dir_root(version_tag: str = None) -> str:
    """
    Get the remote root directory.

    The format of ``version_tag`` should be ``YYYY.MM.DD-VERSION_CODE``.

    The return does **NOT** end with a slash.
    """
    if not version_tag:
        version_tag = REMOTE_VERSION_TAG

    return f"{PATH_REMOTE_GH}{version_tag}"


def get_remote_dir_root_resources(version_tag: str = None) -> str:
    """
    Get the remote root resource directory.

    The format of ``version_tag`` should be ``YYYY.MM.DD-VERSION_CODE``.

    The return does **NOT** end with a slash.
    """
    return f"{get_remote_dir_root(version_tag)}/assets/_gluonresources/resources"
