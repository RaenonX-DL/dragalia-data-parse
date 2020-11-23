import pytest

from tests.static import PATH_DIR_MASTER_ASSET, PATH_DIR_CUSTOM_ASSET


@pytest.fixture
def asset_master_dir() -> str:
    """Get the directory of the master assets."""
    return PATH_DIR_MASTER_ASSET


@pytest.fixture
def asset_custom_dir() -> str:
    """Get the directory of the custom assets."""
    return PATH_DIR_CUSTOM_ASSET
