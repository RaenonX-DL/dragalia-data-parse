from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES

manager = AssetManager(PATH_LOCAL_ROOT_RESOURCES)

hit_attrs_to_check = """
- CAN_126_04_HEAL_LV01
- CAN_126_04_HEAL_LV02
- CAN_126_04_HEAL_LV03
- CAN_126_04_HEAL_PLUS_LV01
- CAN_126_04_HEAL_PLUS_LV02
- CAN_126_04_HEAL_PLUS_LV03
- CAN_126_04_HEAL_SHARE_LV01
- CAN_126_04_HEAL_SHARE_LV02
- CAN_126_04_HEAL_SHARE_LV03
- CAN_126_04_HP_LV01
- CAN_126_04_HP_LV02
- CAN_126_04_HP_LV03
- CAN_126_04_REJENE_LV01
- CAN_126_04_REJENE_LV02
- CAN_126_04_REJENE_LV03
- CAN_127_04_CURE_LV01
- CAN_127_04_CURE_LV02
- CAN_127_04_DPC_LV01
- CAN_127_04_DPC_LV02
- CAN_127_04_DRAIN_LV01
- CAN_127_04_DRAIN_LV02
- CAN_127_04_HEAL_LV01
- CAN_127_04_HEAL_LV02
- CAN_NAM_CHR_01_AURA_LV01
- CAN_NAM_CHR_01_AURA_LV02
- CAN_NAM_CHR_01_H01_LV01
- CAN_NAM_CHR_01_H01_LV02
- CAN_NAM_CHR_01_HEAL_LV01
- CAN_NAM_CHR_01_HEAL_LV02
- CAN_NAM_CMB_01_H01
- CAN_NAM_CMB_02_H01
- CAN_NAM_CMB_03_H01
- CAN_NAM_DAS_02_H01
- S170_000_00
- S170_000_00_2
- S170_000_01
- S170_000_01_2
- S170_000_02
- S170_000_02_2
- S170_001_00_LV01
- S170_001_00_LV02
- S170_001_00_LV03
- S170_001_01_LV01
- S170_001_01_LV02
- S170_001_01_LV03
- S170_001_02_LV01
- S170_001_02_LV02
- S170_001_02_LV03
- S170_002_00_LV01
- S170_002_00_LV02
- S170_002_01_LV01
- S170_002_01_LV02
"""


def check_hit_attr_data(asset_manager: AssetManager, hit_attr_labels: list[str]):
    for hit_attr_label in hit_attr_labels:
        hit_attr_label = hit_attr_label.replace("-", "").strip()

        hit_attr_data = asset_manager.asset_hit_attr.get_data_by_id(hit_attr_label)

        print(f"{hit_attr_label:<30} | "
              f"Damage Modifier: {hit_attr_data.damage_modifier:>10.3f} | "
              f"ODx: {hit_attr_data.rate_boost_od:>5.3f} | "
              f"Ability Condition ID: {hit_attr_data.action_condition_id}")


def main():
    check_hit_attr_data(manager, hit_attrs_to_check.strip().split("\n"))


if __name__ == '__main__':
    main()
