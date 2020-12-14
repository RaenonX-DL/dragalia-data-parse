import pytest

from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer, SkillTransformer
from tests.static import PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET, PATH_LOCAL_DIR_MASTER_ASSET

_asset_manager: AssetManager = AssetManager(
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
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


# endregion


# region Asset Manager fixtures

@pytest.fixture
def asset_manager() -> AssetManager:
    """Get the asset manager containing all the available asset instances."""
    return _asset_manager


# endregion


# region `pytest` hooks
def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", dest="slow",
                     default=False, help="Specify this flag to run the slow tests.")


def pytest_configure(config):
    if not config.option.slow:
        setattr(config.option, "markexpr", (getattr(config.option, "markexpr", "") + " not slow").strip())
# endregion
