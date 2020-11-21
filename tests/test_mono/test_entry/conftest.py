import pytest

from dlparse.mono.asset import CharaModeAsset, TextAsset
from tests.static import PATH_MASTER_ASSET_DIR

# Asset instances
_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=PATH_MASTER_ASSET_DIR)
_text: TextAsset = TextAsset(asset_dir=PATH_MASTER_ASSET_DIR)


@pytest.fixture
def chara_mode_asset() -> CharaModeAsset:
    """Get the character mode data asset."""
    return _chara_mode


@pytest.fixture
def text_asset() -> TextAsset:
    """Get the text label asset."""
    return _text
