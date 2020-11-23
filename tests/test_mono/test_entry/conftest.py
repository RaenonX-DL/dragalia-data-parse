import pytest

from dlparse.mono.asset import CharaModeAsset, TextAsset
from tests.static import PATH_DIR_MASTER_ASSET

# Asset instances
_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_text: TextAsset = TextAsset(asset_dir=PATH_DIR_MASTER_ASSET)


@pytest.fixture
def chara_mode_asset() -> CharaModeAsset:
    """Get the character mode data asset."""
    return _chara_mode


@pytest.fixture
def text_asset() -> TextAsset:
    """Get the text label asset."""
    return _text
