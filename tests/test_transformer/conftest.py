import pytest

from dlparse.mono.asset import SkillDataAsset, HitAttrAsset
from dlparse.mono.path import PlayerActionFilePathFinder
from dlparse.transformer import SkillTransformer
from tests.static import PATH_MASTER_ASSET_DIR, PATH_PLAYER_ACTION_ASSET_ROOT

# Asset instances
_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=PATH_MASTER_ASSET_DIR)
_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=PATH_MASTER_ASSET_DIR)
_pa_path_finder: PlayerActionFilePathFinder = PlayerActionFilePathFinder(PATH_PLAYER_ACTION_ASSET_ROOT)

# Transformets
_transformer_skill: SkillTransformer = SkillTransformer(_skill_data, _hit_attr, _pa_path_finder)


@pytest.fixture
def transformer_skill():
    """Get the skill transformer."""
    return _transformer_skill
