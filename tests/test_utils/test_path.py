import os

import pytest

from dlparse.enums import Language
from dlparse.errors import PathUnlocalizableError
from dlparse.utils import localize_asset_path, localize_path
from tests.static import get_remote_dir_root, get_remote_dir_root_resources


def test_localize_throw_error_if_no_matching_pattern():
    with pytest.raises(PathUnlocalizableError):
        localize_asset_path(os.path.join("a", "b"), Language.EN)


def test_localize_return_correct():
    localized = localize_asset_path(os.path.join("media", "assets"), Language.EN)
    assert localized == os.path.join("media", "localized", "en", "assets")


def test_localize_return_original_for_master():
    localized = localize_asset_path(os.path.join("media", "assets"), Language.JP)
    assert localized == os.path.join("media", "assets")


def test_localize_not_using_backslash_if_network():
    localized = localize_asset_path(get_remote_dir_root_resources(), Language.EN)
    assert localized == f"{get_remote_dir_root()}/localized/en/assets/_gluonresources/resources"


def test_localize_path():
    localized = localize_path(os.path.join("a", "b"), Language.CHT)
    assert localized == os.path.join("localized", Language.CHT, "a", "b")


def test_localize_path_trailing_slash():
    localized = localize_path(os.path.join("a", "b") + os.sep, Language.CHT)
    assert localized == os.path.join("localized", Language.CHT, "a", "b") + os.sep


def test_localize_path_file():
    localized = localize_path(os.path.join("a", "b", "c.json"), Language.CHT)
    assert localized == os.path.join("localized", Language.CHT, "a", "b", "c.json")
