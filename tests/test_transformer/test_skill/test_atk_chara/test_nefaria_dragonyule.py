import pytest

from dlparse.errors import HitDataUnavailableError
from dlparse.transformer import SkillTransformer


def test_s2_no_atk_data(transformer_skill: SkillTransformer):
    # Dragonyule Nefaria S2
    # https://dragalialost.wiki/w/Dragonyule_Nefaria
    with pytest.raises(HitDataUnavailableError):
        transformer_skill.transform_attacking(106402022)
