import pytest

from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer, EnemyTransformer, QuestTransformer, SkillTransformer
from tests.static import (
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_CHARA_MOTION_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET,
    PATH_LOCAL_DIR_DRAGON_MOTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
)

_asset_manager: AssetManager = AssetManager(
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
    PATH_LOCAL_DIR_CHARA_MOTION_ASSET, PATH_LOCAL_DIR_DRAGON_MOTION_ASSET,
    custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)


# region Transformer fixtures

@pytest.fixture
def transformer_skill() -> SkillTransformer:
    """Get the skill transformer."""
    return _asset_manager.transformer_skill


@pytest.fixture
def transformer_ability() -> AbilityTransformer:
    """Get the ability transformer."""
    return _asset_manager.transformer_ability


@pytest.fixture
def transformer_enemy() -> EnemyTransformer:
    """Get the enemy data transformer."""
    return _asset_manager.transformer_enemy


@pytest.fixture
def transformer_quest() -> QuestTransformer:
    """Get the quest data transformer."""
    return _asset_manager.transformer_quest


# endregion


# region Asset Manager fixtures

@pytest.fixture
def asset_manager() -> AssetManager:
    """Get the asset manager containing all the available asset instances."""
    return _asset_manager


# endregion


# region `pytest` hooks
def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", dest="slow", default=False,
                     help="Specify this flag to run slow tests.")
    parser.addoption("--holistic", action="store_true", dest="holistic", default=False,
                     help="Specify this flag to run holistic tests.")
    parser.addoption("--all", action="store_true", dest="all", default=False,
                     help="Specify this flag to run all tests, "
                          "including the one that is either marked as `slow` or `holistic`.")


def pytest_configure(config):
    if not config.option.all:
        marks = []

        if not config.option.slow:
            marks.append("not slow")
        if not config.option.holistic:
            marks.append("not holistic")

        setattr(config.option, "markexpr", (getattr(config.option, "markexpr", "") + " and ".join(marks)).strip())
# endregion
