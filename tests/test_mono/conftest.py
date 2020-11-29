import pytest

from dlparse.mono.asset import CharaModeAsset, CharaDataAsset, TextAsset, SkillDataAsset
from tests.static import PATH_DIR_MASTER_ASSET

# Asset instances
_chara_data: CharaDataAsset = CharaDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_text: TextAsset = TextAsset(asset_dir=PATH_DIR_MASTER_ASSET)


@pytest.fixture
def chara_asset() -> CharaDataAsset:
    """Get the character data asset."""
    return _chara_data


@pytest.fixture
def chara_mode_asset() -> CharaModeAsset:
    """Get the character mode data asset."""
    return _chara_mode


@pytest.fixture
def skill_asset() -> SkillDataAsset:
    """Get the skill data asset."""
    return _skill_data


@pytest.fixture
def text_asset() -> TextAsset:
    """Get the text label asset."""
    return _text
