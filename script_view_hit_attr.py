from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET, PATH_LOCAL_DIR_MASTER_ASSET

manager = AssetManager(
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
    custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)

hit_attrs_to_check = """
LAN_127_04_H01_2_LV01
LAN_127_04_H01_2_LV01
LAN_127_04_H01_2_LV01
LAN_127_04_DISPEL_LV01
LAN_127_04_ALLY_LV01
LAN_127_04_H02_1_LV01
LAN_127_04_H02_2_LV01
LAN_127_04_H02_3_LV01
LAN_127_04_1_TENSION_LV01
LAN_127_04_2_TENSION_LV01
LAN_127_04_3_TENSION_LV01
"""


def check_hit_attr_data(asset_manager: AssetManager, hit_attr_labels: list[str]):
    for hit_attr_label in hit_attr_labels:
        hit_attr_data = asset_manager.asset_hit_attr.get_data_by_id(hit_attr_label)

        print(f"{hit_attr_label:<30} | "
              f"Damage Modifier: {hit_attr_data.damage_modifier:>10.3f} | "
              f"Ability Condition ID: {hit_attr_data.action_condition_id}")


def main():
    check_hit_attr_data(manager, hit_attrs_to_check.strip().split("\n"))


if __name__ == '__main__':
    main()
