import pytest

from dlparse.mono.asset import (
    ActionConditionAsset, CharaDataAsset, CharaModeAsset, HitAttrAsset, SkillDataAsset, TextAsset,
)
from dlparse.mono.loader import PlayerActionFileLoader
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.static import PATH_DIR_CUSTOM_ASSET, PATH_DIR_MASTER_ASSET, PATH_ROOT_ASSET_PLAYER_ACTION

_asset_manager: AssetManager = AssetManager(
    PATH_ROOT_ASSET_PLAYER_ACTION, PATH_DIR_MASTER_ASSET, PATH_DIR_CUSTOM_ASSET
)


# region Directory fixtures

@pytest.fixture
def asset_master_dir() -> str:
    """Get the directory of the master assets."""
    return PATH_DIR_MASTER_ASSET


@pytest.fixture
def asset_custom_dir() -> str:
    """Get the directory of the custom assets."""
    return PATH_DIR_CUSTOM_ASSET

# endregion


# region Asset fixtures

@pytest.fixture
def asset_action_cond() -> ActionConditionAsset:
    """Get the action condition data asset."""
    return _asset_manager.asset_action_cond


@pytest.fixture
def asset_chara() -> CharaDataAsset:
    """Get the character data asset."""
    return _asset_manager.asset_chara_data


@pytest.fixture
def asset_chara_mode() -> CharaModeAsset:
    """Get the character mode data asset."""
    return _asset_manager.asset_chara_mode


@pytest.fixture
def asset_hit_attr() -> HitAttrAsset:
    """Get the hit attribute data asset."""
    return _asset_manager.asset_hit_attr


@pytest.fixture
def asset_skill() -> SkillDataAsset:
    """Get the skill data asset."""
    return _asset_manager.asset_skill


@pytest.fixture
def asset_text() -> TextAsset:
    """Get the text label asset."""
    return _asset_manager.asset_text


# endregion


# region Loader fixtures

@pytest.fixture
def loader_action() -> PlayerActionFileLoader:
    """Get the player action file loader."""
    return _asset_manager.loader_pa


# endregion


# region Transformer fixtures

@pytest.fixture
def transformer_skill() -> SkillTransformer:
    """Get the skill transformer."""
    return _asset_manager.transformer_skill


# endregion


# region Asset Manager fixtures

@pytest.fixture
def asset_manager() -> AssetManager:
    """Get the asset manager containing all the available asset instances."""
    return _asset_manager

# endregion
