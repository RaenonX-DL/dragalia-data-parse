import pytest

from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES, get_remote_dir_root_resources


@pytest.mark.slow
def test_load_local_dir():
    manager = AssetManager(PATH_LOCAL_ROOT_RESOURCES)
    assert "CHARA_NAME_19900001" in manager.asset_text


@pytest.mark.slow
def test_load_remote_dir():
    manager = AssetManager(get_remote_dir_root_resources(), is_network_source=True)
    assert "CHARA_NAME_19900001" in manager.asset_text
