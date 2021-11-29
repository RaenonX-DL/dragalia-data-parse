from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES

manager = AssetManager(PATH_LOCAL_ROOT_RESOURCES)

hit_attrs_to_check = """
- S164_000_00
- S164_001_00_LV01
- S164_001_00_LV02
- S164_001_01_LV01
- S164_001_01_LV02
- S164_002_00
- S164_002_01
- S164_003_00
- S164_003_01_LV01
- S164_003_01_LV02
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
