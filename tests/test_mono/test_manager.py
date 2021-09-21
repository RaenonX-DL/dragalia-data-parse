import pytest

from dlparse.enums import Language
from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES, get_remote_dir_root_resources


@pytest.mark.slow
def test_load_local_dir():
    manager = AssetManager(PATH_LOCAL_ROOT_RESOURCES)
    assert manager.asset_text_multi.get_text(Language.JP, "CHARA_NAME_19900001") is not None


@pytest.mark.slow
def test_load_remote_dir():
    manager = AssetManager(get_remote_dir_root_resources(), is_network_source=True)
    assert manager.asset_text_multi.get_text(Language.JP, "CHARA_NAME_19900001") is not None
