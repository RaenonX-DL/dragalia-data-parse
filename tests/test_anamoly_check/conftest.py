import pytest

from dlparse.mono.asset import SkillDataAsset, HitAttrAsset, CharaDataAsset, CharaModeAsset, ActionConditionAsset
from dlparse.mono.loader import PlayerActionFileLoader
from dlparse.transformer import SkillTransformer
from tests.static import PATH_DIR_MASTER_ASSET, PATH_ROOT_ASSET_PLAYER_ACTION

# Asset instances
_chara_data: CharaDataAsset = CharaDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_action_cond: ActionConditionAsset = ActionConditionAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_pa_loader: PlayerActionFileLoader = PlayerActionFileLoader(PATH_ROOT_ASSET_PLAYER_ACTION)

# Transformets
_transformer_skill: SkillTransformer = SkillTransformer(_skill_data, _hit_attr, _action_cond, _pa_loader)


@pytest.fixture
def transformer_skill() -> SkillTransformer:
    """Get the skill transformer."""
    return _transformer_skill


@pytest.fixture
def asset_skill() -> SkillDataAsset:
    """Get the skill data asset."""
    return _skill_data


@pytest.fixture
def asset_chara() -> CharaDataAsset:
    """Get the character data asset."""
    return _chara_data


@pytest.fixture
def asset_chara_mode() -> CharaModeAsset:
    """Get the character mode data asset."""
    return _chara_mode
