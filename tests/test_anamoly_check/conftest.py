import pytest

from dlparse.mono.asset import SkillDataAsset, HitAttrAsset, CharaDataAsset, CharaModeAsset
from dlparse.mono.loader import PlayerActionFileLoader
from dlparse.transformer import SkillTransformer
from tests.static import PATH_MASTER_ASSET_DIR, PATH_PLAYER_ACTION_ASSET_ROOT

# Asset instances
_chara_data: CharaDataAsset = CharaDataAsset(asset_dir=PATH_MASTER_ASSET_DIR)
_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=PATH_MASTER_ASSET_DIR)
_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=PATH_MASTER_ASSET_DIR)
_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=PATH_MASTER_ASSET_DIR)
_pa_path_finder: PlayerActionFileLoader = PlayerActionFileLoader(PATH_PLAYER_ACTION_ASSET_ROOT)

# Transformets
_transformer_skill: SkillTransformer = SkillTransformer(_skill_data, _hit_attr, _pa_path_finder)


@pytest.fixture
def transformer_skill() -> SkillTransformer:
    """Get the skill transformer."""
    return _transformer_skill


@pytest.fixture
def asset_chara_data() -> CharaDataAsset:
    """Get the character data asset."""
    return _chara_data


@pytest.fixture
def asset_chara_mode() -> CharaModeAsset:
    """Get the character mode data asset."""
    return _chara_mode
