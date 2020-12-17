import pytest

from dlparse.errors import HitDataUnavailableError
from dlparse.transformer import SkillTransformer


def test_no_hit_data(transformer_skill: SkillTransformer):
    # Patia S1 as ATK
    # https://dragalialost.gamepedia.com/Patia
    with pytest.raises(HitDataUnavailableError):
        transformer_skill.transform_attacking(105405021)
