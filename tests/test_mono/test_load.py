import os

import pytest

from dlparse.mono.asset import TextAsset
from dlparse.mono.loader import ActionFileLoader
from dlparse.mono.manager import AssetManager
from tests.static import (
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET, get_remote_dir_action_asset, get_remote_dir_master_asset,
)


def test_load_file_like():
    with open(os.path.join(PATH_LOCAL_DIR_MASTER_ASSET, "TextLabel.json"), encoding="utf-8") as f:
        asset = TextAsset(file_like=f)
    assert "CHARA_NAME_19900001" in asset


def test_load_local_dir():
    asset = TextAsset(asset_dir=PATH_LOCAL_DIR_MASTER_ASSET)
    assert "CHARA_NAME_19900001" in asset


def test_load_local_file():
    asset = TextAsset(os.path.join(PATH_LOCAL_DIR_MASTER_ASSET, "TextLabel.json"))
    assert "CHARA_NAME_19900001" in asset


@pytest.mark.slow
def test_load_remote_dir():
    asset = TextAsset(asset_dir=get_remote_dir_master_asset())
    assert "CHARA_NAME_19900001" in asset


@pytest.mark.slow
def test_load_remote_file():
    asset = TextAsset(get_remote_dir_master_asset() + "/TextLabel.json")
    assert "CHARA_NAME_19900001" in asset


def test_prefab_loader_local_dir(asset_manager: AssetManager):
    loader = ActionFileLoader(asset_manager.asset_action_list, PATH_LOCAL_DIR_ACTION_ASSET)
    assert loader.get_prefab(141001) is not None


@pytest.mark.slow
def test_prefab_loader_remote_dir(asset_manager: AssetManager):
    loader = ActionFileLoader(
        asset_manager.asset_action_list, get_remote_dir_action_asset()
    )
    assert loader.get_prefab(141001) is not None
