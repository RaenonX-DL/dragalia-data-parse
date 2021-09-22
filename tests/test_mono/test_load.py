import os

import pytest

from dlparse.mono.asset import CharaDataAsset
from dlparse.mono.loader import ActionFileLoader
from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES, get_remote_dir_root_resources


def test_load_file_like():
    with open(os.path.join(PATH_LOCAL_ROOT_RESOURCES, "master", "CharaData.json"), encoding="utf-8") as f:
        asset = CharaDataAsset(file_like=f)
    assert 10440501 in asset


def test_load_local_dir():
    asset = CharaDataAsset(asset_dir=os.path.join(PATH_LOCAL_ROOT_RESOURCES, "master"))
    assert 10440501 in asset


def test_load_local_file():
    asset = CharaDataAsset(os.path.join(PATH_LOCAL_ROOT_RESOURCES, "master", "CharaData.json"))
    assert 10440501 in asset


@pytest.mark.slow
def test_load_remote_dir():
    asset = CharaDataAsset(asset_dir=get_remote_dir_root_resources() + "/master")
    assert 10440501 in asset


@pytest.mark.slow
def test_load_remote_file():
    asset = CharaDataAsset(get_remote_dir_root_resources() + "/master/CharaData.json")
    assert 10440501 in asset


def test_prefab_loader_local_dir(asset_manager: AssetManager):
    loader = ActionFileLoader(asset_manager.asset_action_list, os.path.join(PATH_LOCAL_ROOT_RESOURCES, "actions"))
    assert loader.get_prefab(141001) is not None


@pytest.mark.slow
def test_prefab_loader_remote_dir(asset_manager: AssetManager):
    loader = ActionFileLoader(asset_manager.asset_action_list, get_remote_dir_root_resources() + "/actions")
    assert loader.get_prefab(141001) is not None
