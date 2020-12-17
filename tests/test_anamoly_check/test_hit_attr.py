import pytest

from dlparse.mono.manager import AssetManager


def test_bk_special_rate_fs_only(asset_manager: AssetManager):
    non_fs_rate_boost: list[tuple[str, float]] = []

    for hit_attr_data in asset_manager.asset_hit_attr:
        id_is_fs = "CHR" in hit_attr_data.id or "BUR" in hit_attr_data.id
        if not id_is_fs and hit_attr_data.rate_boost_in_bk and hit_attr_data.rate_boost_in_bk != 1:
            non_fs_rate_boost.append((hit_attr_data.id, hit_attr_data.rate_boost_in_bk))

    if non_fs_rate_boost:
        message_str = "\n".join(f"- {label} ({rate})" for label, rate in non_fs_rate_boost)

        pytest.fail(f"Some non-FS hit attributes have special BK rate: {message_str}")


def test_no_od_special_rate(asset_manager: AssetManager):
    od_rate_boost: list[tuple[str, float]] = []

    for hit_attr_data in asset_manager.asset_hit_attr:
        if hit_attr_data.rate_boost_in_od and hit_attr_data.rate_boost_in_od != 1:
            od_rate_boost.append((hit_attr_data.id, hit_attr_data.rate_boost_in_od))

    if od_rate_boost:
        message_str = "\n".join(f"- {label} ({rate})" for label, rate in od_rate_boost)

        pytest.fail(f"Some hit attributes have special OD rate: {message_str}")
