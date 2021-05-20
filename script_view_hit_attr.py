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
- GUN_115_04_BUF_LV01
- GUN_115_04_BUF_LV02
- GUN_115_04_BUF_LV03
- GUN_115_04_DEL_LV01
- GUN_115_04_DEL_LV02
- GUN_115_04_DEL_LV03
- GUN_115_04_H01_LV01
- GUN_115_04_H01_LV02
- GUN_115_04_H01_LV03
- GUN_115_04_PLUS_H01_LV01
- GUN_115_04_PLUS_H01_LV02
- GUN_115_04_PLUS_H01_LV03
- GUN_116_04_BUF_LV01
- GUN_116_04_BUF_LV02
- GUN_116_04_DISPEL_LV01
- GUN_116_04_DISPEL_LV02
- GUN_116_04_PLUS_BUF_LV01
- GUN_116_04_PLUS_BUF_LV02
- KAT_126_04_BUF_LV01
- KAT_126_04_BUF_LV02
- KAT_126_04_BUF_LV03
- KAT_127_04_BUF_LV01
- KAT_127_04_BUF_LV02
- KAT_127_04_BUF_LV03
- KAT_127_04_H00_LV01
- KAT_127_04_H00_LV02
- KAT_127_04_H00_LV03
- KAT_127_04_H01_LV01
- KAT_127_04_H01_LV02
- KAT_127_04_H01_LV03
- KAT_127_04_H02_LV01
- KAT_127_04_H02_LV02
- KAT_127_04_H02_LV03
- KAT_CHR_13_H01_LV01
- KAT_CHR_13_H01_LV01_CHLV02
- KAT_CHR_13_H01_LV02
- KAT_CHR_13_H01_LV02_CHLV02
- KAT_CHR_14_H01_LV01
- KAT_CHR_14_H01_LV01_CHLV02
- KAT_CHR_14_H01_LV02
- KAT_CHR_14_H01_LV02_CHLV02
- KAT_CHR_14_H02_LV01_CHLV02
- KAT_CHR_14_H02_LV02_CHLV02
- KAT_CHR_15_H01_LV01
- KAT_CHR_15_H01_LV01_CHLV02
- KAT_CHR_15_H01_LV02
- KAT_CHR_15_H01_LV02_CHLV02
- KAT_CHR_15_H02_LV01_CHLV02
- KAT_CHR_15_H02_LV02_CHLV02
- KAT_CHR_16_H01_LV01
- KAT_CHR_16_H01_LV01_CHLV02
- KAT_CHR_16_H01_LV02
- KAT_CHR_16_H01_LV02_CHLV02
- KAT_CHR_16_H02_LV01_CHLV02
- KAT_CHR_16_H02_LV02_CHLV02
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
