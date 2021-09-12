import os

import pytest

from dlparse.enums import Language
from dlparse.errors import PathUnlocalizableError
from dlparse.utils import localize_asset_path


def test_localize_throw_error_if_no_matching_pattern():
    with pytest.raises(PathUnlocalizableError):
        localize_asset_path(os.path.join("a", "b"), Language.EN)


def test_localize_return_correct():
    localized = localize_asset_path(os.path.join("media", "assets"), Language.EN)
    assert localized == os.path.join("media", "localized", "en", "assets")


def test_localize_return_original_for_master():
    localized = localize_asset_path(os.path.join("media", "assets"), Language.JP)
    assert localized == os.path.join("media", "assets")
