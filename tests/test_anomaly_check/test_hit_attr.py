import pytest

from dlparse.mono.manager import AssetManager


def test_special_od_rate_fs_only(asset_manager: AssetManager):
    non_fs_rate_boost: list[tuple[str, float]] = []

    for hit_attr_data in asset_manager.asset_hit_attr:
        id_is_fs = "CHR" in hit_attr_data.id or "BUR" in hit_attr_data.id
        if not id_is_fs and hit_attr_data.rate_boost_od and hit_attr_data.rate_boost_od != 1:
            non_fs_rate_boost.append((hit_attr_data.id, hit_attr_data.rate_boost_od))

    if non_fs_rate_boost:
        message_str = "\n".join(f"- {label} ({rate})" for label, rate in non_fs_rate_boost)

        pytest.fail(f"Some non-FS hit attributes have special OD rate: {message_str}")


def test_no_normal_special_rate(asset_manager: AssetManager):
    normal_rate_boost: list[tuple[str, float]] = []

    for hit_attr_data in asset_manager.asset_hit_attr:
        if hit_attr_data.rate_boost_normal and hit_attr_data.rate_boost_normal != 1:
            normal_rate_boost.append((hit_attr_data.id, hit_attr_data.rate_boost_normal))

    if normal_rate_boost:
        message_str = "\n".join(f"- {label} ({rate})" for label, rate in normal_rate_boost)

        pytest.fail(f"Some hit attributes have special normal state rate: {message_str}")
