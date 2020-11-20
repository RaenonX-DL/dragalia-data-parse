import pytest

from tests.static import PATH_MASTER_ASSET_DIR


@pytest.fixture
def asset_master_dir():
    """Get the directory of the master assets."""
    return PATH_MASTER_ASSET_DIR
