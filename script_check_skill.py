from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_DIR_CUSTOM_ASSET, PATH_LOCAL_ROOT_RESOURCES, get_remote_dir_root_resources

version_tag = "2021.09.13-a0etJGKf8G7Y1gKy"

manager_local = AssetManager(PATH_LOCAL_ROOT_RESOURCES, custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET)
manager_remote = AssetManager(
    get_remote_dir_root_resources(version_tag),
    is_network_source=True, custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)


def check_unparsed_skill(old_asset: AssetManager, new_asset: AssetManager):
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


def main():
    check_unparsed_skill(manager_remote, manager_local)


if __name__ == '__main__':
    main()
