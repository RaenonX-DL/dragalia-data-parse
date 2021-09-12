import os

import pytest

from dlparse.mono.asset import TextAsset
from tests.static import PATH_LOCAL_DIR_CUSTOM_ASSET, PATH_LOCAL_ROOT_RESOURCES, get_remote_dir_root_resources


def test_override_local():
    asset_text = TextAsset(
        asset_dir=os.path.join(PATH_LOCAL_ROOT_RESOURCES, "master"),
        custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
    )

    assert asset_text.to_text("TEST_TEXT_LABEL") == "Test"


@pytest.mark.slow
def test_override_mix():
    asset_text = TextAsset(get_remote_dir_root_resources(), custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET)

    assert asset_text.to_text("TEST_TEXT_LABEL") == "Test"
