import pytest

from dlparse.mono.asset import TextAsset
from tests.static import (PATH_LOCAL_DIR_CUSTOM_ASSET, PATH_LOCAL_DIR_MASTER_ASSET, get_remote_dir_master_asset)


def test_override_local():
    asset_text = TextAsset(asset_dir=PATH_LOCAL_DIR_MASTER_ASSET, custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET)

    assert asset_text.to_text("TEST_TEXT_LABEL") == "Test"


@pytest.mark.slow
def test_override_mix():
    asset_text = TextAsset(asset_dir=get_remote_dir_master_asset(), custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET)

    assert asset_text.to_text("TEST_TEXT_LABEL") == "Test"
