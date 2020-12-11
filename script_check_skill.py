from dlparse.mono.asset import CharaDataEntry, SkillDataEntry
from dlparse.mono.asset.base import MasterAssetBase
from dlparse.mono.manager import AssetManager
from tests.static import (
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET, PATH_LOCAL_DIR_MASTER_ASSET, get_remote_dir_action_asset,
    get_remote_dir_master_asset,
)

version_tag = "2020.11.23-08NV7KO9YyXMIlB2"

manager_local = AssetManager(
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
    custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)
manager_remote = AssetManager(
    get_remote_dir_action_asset(version_tag), get_remote_dir_master_asset(version_tag),
    custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)


def check_diff_internal(left: MasterAssetBase, right: MasterAssetBase, title: str, manager: AssetManager):
    if diff_ids := (left.all_ids - right.all_ids):
        print(f"{title} in {left.__class__.__name__} ({len(diff_ids)}):")

        for diff_id in sorted(diff_ids):
            data = left.get_data_by_id(diff_id)
            if isinstance(data, SkillDataEntry):
                print(f"- {diff_id} ({manager.asset_text.to_text(data.name_label)})")
            elif isinstance(data, CharaDataEntry):
                print(f"- {diff_id} ({data.get_chara_name(manager.asset_text)})")
            else:
                print(f"- {diff_id}")

        print()


def check_diff(old_asset: AssetManager, new_asset: AssetManager):
    diff_chara_ids = new_asset.asset_chara_data.all_ids - old_asset.asset_chara_data.all_ids
    diff_skill_ids = new_asset.asset_skill_data.all_ids - old_asset.asset_skill_data.all_ids

    for chara_id in diff_chara_ids:
        print(f"New character ID: {chara_id}")
        print()

        chara_data = new_asset.asset_chara_data.get_data_by_id(chara_id)
        diff_skill_ids -= {id_entry.skill_id for id_entry in chara_data.get_skill_id_entries(new_asset)}

    if diff_skill_ids:
        print("!" * 20 + f" WARNING - UNPARSED SKILLS DETECTED ({len(diff_skill_ids)}) " + "!" * 20)
        for skill_id in diff_skill_ids:
            print(skill_id)


if __name__ == '__main__':
    check_diff(manager_remote, manager_local)
