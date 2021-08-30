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
- S161_000_00
- S161_000_01
- S161_000_02
- S161_002_00_LV02
- S161_002_01_LV02
- S161_002_02_LV02
- S161_002_03_LV02
- S161_003_00
- S161_003_01
- S161_003_02
- S161_003_02_DRAIN
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
