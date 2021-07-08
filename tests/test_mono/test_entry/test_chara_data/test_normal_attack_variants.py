from dlparse.enums import Weapon
from dlparse.mono.manager import AssetManager

from .utils import create_dummy


def test_no_mode(asset_manager: AssetManager):
    entry = create_dummy()

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 1
    assert variants[0] == (0, 100000)


def test_no_mode_axe(asset_manager: AssetManager):
    entry = create_dummy(weapon=Weapon.AXE)

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 1
    assert variants[0] == (0, 400000)


def test_unique_transform_has_default(asset_manager: AssetManager):
    entry = create_dummy(mode_1_id=0, mode_2_id=20, weapon=Weapon.AXE)

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 2
    assert variants[0] == (0, 400000)
    assert variants[1] == (20, 700200)


def test_unique_transform_no_default(asset_manager: AssetManager):
    entry = create_dummy(mode_1_id=19, mode_2_id=20, weapon=Weapon.AXE)

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 2
    assert variants[0] == (19, 300400)
    assert variants[1] == (20, 700200)


def test_button_has_default(asset_manager: AssetManager):
    entry = create_dummy(mode_1_id=0, mode_2_id=20, mode_3_id=22, weapon=Weapon.AXE)

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 3
    assert variants[0] == (0, 400000)
    assert variants[1] == (20, 700200)
    assert variants[2] == (22, 100200)


def test_button_all_special(asset_manager: AssetManager):
    entry = create_dummy(mode_1_id=19, mode_2_id=20, mode_3_id=22, weapon=Weapon.AXE)

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 3
    assert variants[0] == (19, 300400)
    assert variants[1] == (20, 700200)
    assert variants[2] == (22, 100200)


def test_all_modes_in_use(asset_manager: AssetManager):
    entry = create_dummy(mode_1_id=19, mode_2_id=20, mode_3_id=22, mode_4_id=23, weapon=Weapon.AXE)

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 4
    assert variants[0] == (19, 300400)
    assert variants[1] == (20, 700200)
    assert variants[2] == (22, 100200)
    assert variants[3] == (23, 100300)


def test_mode_without_unique_combo(asset_manager: AssetManager):
    entry = create_dummy(mode_1_id=19, mode_2_id=20, mode_3_id=21, weapon=Weapon.AXE)

    variants = list(entry.get_normal_attack_variants(asset_manager))
    assert len(variants) == 2
    assert variants[0] == (19, 300400)
    assert variants[1] == (20, 700200)
