from dlparse.mono.manager import AssetManager
from tests.static import (
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_CHARA_MOTION_ASSET, PATH_LOCAL_DIR_CUSTOM_ASSET,
    PATH_LOCAL_DIR_DRAGON_MOTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
)

manager = AssetManager(
    PATH_LOCAL_DIR_ACTION_ASSET, PATH_LOCAL_DIR_MASTER_ASSET,
    PATH_LOCAL_DIR_CHARA_MOTION_ASSET, PATH_LOCAL_DIR_DRAGON_MOTION_ASSET,
    custom_asset_dir=PATH_LOCAL_DIR_CUSTOM_ASSET
)

hit_attrs_to_check = """
- LAN_138_04_H01_LV01
- LAN_138_04_H01_LV02
- LAN_138_04_H01_LV03
- LAN_138_04_H02_LV01
- LAN_138_04_H02_LV02
- LAN_138_04_H02_LV03
- LAN_138_04_PLUS_H00_LV01
- LAN_138_04_PLUS_H00_LV02
- LAN_138_04_PLUS_H00_LV03
- LAN_138_04_PLUS_H01_LV01
- LAN_138_04_PLUS_H01_LV02
- LAN_138_04_PLUS_H01_LV03
- LAN_138_04_PLUS_H02_LV01
- LAN_138_04_PLUS_H02_LV02
- LAN_138_04_PLUS_H02_LV03
- LAN_138_04_PLUS_H03_LV01
- LAN_138_04_PLUS_H03_LV02
- LAN_138_04_PLUS_H03_LV03
- LAN_139_04_H01_LV01
- LAN_139_04_H01_LV02
- LAN_139_04_H02_LV01
- LAN_139_04_H02_LV02
- LAN_140_04_H01_LV01
- LAN_GRI_CMB_01_H01
- LAN_GRI_CMB_02_H01
- LAN_GRI_CMB_03_H01
- LAN_GRI_CMB_04_H01
- LAN_GRI_CMB_05_H01
- S152_000_00
- S152_000_01
- S152_000_02
- S152_001_00_LV01
- S152_001_00_LV02
- S152_001_01_LV01
- S152_001_01_LV02
- S152_002_00_LV01
- S152_002_00_LV02
- S152_002_01_LV01
- S152_002_01_LV02
"""


def check_hit_attr_data(asset_manager: AssetManager, hit_attr_labels: list[str]):
    for hit_attr_label in hit_attr_labels:
        hit_attr_label = hit_attr_label.replace("-", "").strip()

        hit_attr_data = asset_manager.asset_hit_attr.get_data_by_id(hit_attr_label)

        print(f"{hit_attr_label:<30} | "
              f"Damage Modifier: {hit_attr_data.damage_modifier:>10.3f} | "
              f"Ability Condition ID: {hit_attr_data.action_condition_id}")


def main():
    check_hit_attr_data(manager, hit_attrs_to_check.strip().split("\n"))


if __name__ == '__main__':
    main()
