import pytest

from dlparse.mono.asset import SkillDataAsset, HitAttrAsset
from dlparse.mono.loader import PlayerActionFileLoader
from dlparse.transformer import SkillTransformer
from tests.static import PATH_DIR_MASTER_ASSET, PATH_ROOT_ASSET_PLAYER_ACTION

# Asset instances
_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_pa_path_finder: PlayerActionFileLoader = PlayerActionFileLoader(PATH_ROOT_ASSET_PLAYER_ACTION)

# Transformets
_transformer_skill: SkillTransformer = SkillTransformer(_skill_data, _hit_attr, _pa_path_finder)


@pytest.fixture
def transformer_skill() -> SkillTransformer:
    """Get the skill transformer."""
    return _transformer_skill
