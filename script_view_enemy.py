from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES

manager = AssetManager(PATH_LOCAL_ROOT_RESOURCES)

enemy_params_to_check = """
- 204380101
- 204380102
- 204380103
- 204380104
- 204380105
- 204380106
"""


def check_enemy_data(asset_manager: AssetManager, enemy_param_ids: list[str]):
    for enemy_param_id in enemy_param_ids:
        enemy_param_id = enemy_param_id.replace("-", "").strip()

        enemy_param = asset_manager.asset_enemy_param.get_data_by_id(int(enemy_param_id))
        enemy_data = asset_manager.asset_enemy_data.get_data_by_id(enemy_param.enemy_data_id)

        print(f"{enemy_param_id} | "
              f"HP: {enemy_param.hp:>10} | "
              f"Base BK: {enemy_param.base_bk:>10} | "
              f"DEF: {enemy_param.defense:>3} | "
              f"BK DEF: {enemy_data.bk_def_rate:>5.2f}")


def main():
    check_enemy_data(manager, enemy_params_to_check.strip().split("\n"))


if __name__ == '__main__':
    main()
