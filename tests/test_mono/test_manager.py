import pytest

from dlparse.mono.manager import AssetManager
from tests.static import (
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET, get_remote_dir_action_asset, get_remote_dir_master_asset,
)


@pytest.mark.slow
def test_load_local_dir():
    manager = AssetManager(PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET)
    assert "CHARA_NAME_19900001" in manager.asset_text


@pytest.mark.slow
def test_load_remote_dir():
    manager = AssetManager(get_remote_dir_action_asset(), get_remote_dir_master_asset())
    assert "CHARA_NAME_19900001" in manager.asset_text
