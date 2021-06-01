from typing import TYPE_CHECKING

from dlparse.mono.asset import CharaDataEntry, SkillDataEntry
from dlparse.mono.manager import AssetManager
from tests.static import (
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_CHARA_MOTION_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET,
    PATH_LOCAL_DIR_DRAGON_MOTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET, get_remote_dir_action_asset,
    get_remote_dir_chara_motion_asset, get_remote_dir_dragon_motion_asset, get_remote_dir_master_asset,
)

if TYPE_CHECKING:
    from dlparse.mono.asset.base import MasterAssetBase

version_tag = "2021.05.27-kB2MLWQWg56aHAXB"

manager_local = AssetManager(
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
    PATH_LOCAL_DIR_CHARA_MOTION_ASSET, PATH_LOCAL_DIR_DRAGON_MOTION_ASSET,
    custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)
manager_remote = AssetManager(
    get_remote_dir_action_asset(version_tag), get_remote_dir_master_asset(version_tag),
    get_remote_dir_chara_motion_asset(version_tag), get_remote_dir_dragon_motion_asset(version_tag),
    custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)


def check_diff_internal(left: "MasterAssetBase", right: "MasterAssetBase", title: str, manager: AssetManager):
    if diff_ids := (left.all_ids - right.all_ids):
        print(f"{title} in {left.__class__.__name__} ({len(diff_ids)}):")

        for diff_id in sorted(diff_ids):
            data = left.get_data_by_id(diff_id)
            if isinstance(data, SkillDataEntry):
                print(f"- {diff_id} ({manager.asset_text.to_text(data.name_label)})")
            elif isinstance(data, CharaDataEntry):
                print(f"- {diff_id} ({data.get_name(manager.asset_text_multi)})")
            else:
                print(f"- {diff_id}")

        print()


def check_diff(old_asset: "MasterAssetBase", new_asset: "MasterAssetBase"):
    type_old = type(old_asset)
    type_new = type(new_asset)

    if type_old is not type_new:
        raise ValueError(f"Types of the assets to compare are not identical: {type_old} / {type_new}")

    print(f"Checking data difference of {type_new.__name__}")
    print()

    check_diff_internal(new_asset, old_asset, "New data", manager_local)
    check_diff_internal(old_asset, new_asset, "Removed data", manager_remote)


def main():
    # check_diff(manager_remote.asset_hit_attr, manager_local.asset_hit_attr)
    # check_diff(manager_remote.asset_skill_data, manager_local.asset_skill_data)
    # check_diff(manager_remote.asset_chara_data, manager_local.asset_chara_data)
    # check_diff(manager_remote.asset_text, manager_local.asset_text)
    check_diff(manager_remote.asset_quest_data, manager_local.asset_quest_data)


if __name__ == '__main__':
    main()
