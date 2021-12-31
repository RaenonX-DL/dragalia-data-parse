from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES

diff_str = """
- 233010101
- 233010102
- 233010103
- 233011101
- 233011102
- 233011103
"""

manager = AssetManager(PATH_LOCAL_ROOT_RESOURCES)


def print_enemy_info(enemy_form, padding=0):
    print(f"{' ' * padding}HP:          {enemy_form.hp:10,} | DEF:      {enemy_form.defense:10}")
    print(f"{' ' * padding}Base OD:     {enemy_form.base_od:10,} | Base BK:  {enemy_form.base_bk:10,}")
    print(f"{' ' * padding}ATK @ OD:    {enemy_form.od_atk_rate:>10.2f} | DEF @ BK: {enemy_form.bk_def_rate:>10.2f}")
    print(f"{' ' * padding}BK Duration:      {enemy_form.bk_duration_sec:5} secs")
    print()
    for status, pct in enemy_form.affliction_resistance_pct.items():
        print(f"{' ' * padding}{status.name:15}: {pct:4}%")


def check_quest(quest_id: int):
    quest_data = manager.transformer_quest.transform_quest_data(quest_id)

    quest_text_cht = manager.asset_text_multi.get_text("cht", quest_data.quest_data.name_view_label)
    quest_text_jp = manager.asset_text_multi.get_text("jp", quest_data.quest_data.name_view_label)
    print(f"#{quest_id:10} - {quest_text_cht} / {quest_text_jp} ({quest_data.quest_mode})")
    print()

    enemy_ids = quest_data.spawn_enemy_param_ids

    for enemy_id in enemy_ids:
        print(f"Enemy #{enemy_id}")
        enemy_data = manager.transformer_enemy.transform_enemy_data(enemy_id)

        for form_idx, enemy_form in enumerate(enemy_data.forms, start=1):
            print()
            print(f"Form #{form_idx}")
            print_enemy_info(enemy_form)

            for child_idx, child in enumerate(enemy_form.children, start=1):
                print()
                print(f"Child #{child_idx}")
                print_enemy_info(child, padding=8)

            for part_idx, part in enumerate(enemy_form.parts, start=1):
                print()
                print(f"Part #{part_idx}")
                print_enemy_info(part, padding=8)

    print("=" * 40)


def main():
    for quest_id in diff_str.strip().split("\n"):
        check_quest(int(quest_id.replace("- ", "")))


if __name__ == '__main__':
    main()
