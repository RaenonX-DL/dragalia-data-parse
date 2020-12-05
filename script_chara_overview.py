from dlparse.mono.manager import AssetManager
from tests.static import PATH_DIR_MASTER_ASSET, PATH_ROOT_ASSET_PLAYER_ACTION

_asset_manager: AssetManager = AssetManager(PATH_ROOT_ASSET_PLAYER_ACTION, PATH_DIR_MASTER_ASSET)


def print_atk_data_entry(chara_data, skill_data, skill_entry):
    print(f"# Attacking effects - Conditions: {skill_entry.condition_comp.conditions_sorted}")
    print()

    for skill_level in range(skill_entry.max_level):
        skill_level_actual = skill_level + 1

        sp_str = f"SP: {skill_data.skill_data_raw.get_sp_at_level(skill_level_actual)}"
        if chara_data.ss_skill_id == skill_data.skill_data_raw.id:
            sp_str += f" / SS SP: {skill_data.skill_data_raw.get_ss_sp_at_level(skill_level_actual)}"

        print(f"Lv.{skill_level_actual} {'(max)' if skill_entry.max_level == skill_level else ''}| {sp_str}")
        print()
        print(f"Mods distribution: {skill_entry.mods[skill_level]}")
        print(f"Total Mods: {skill_entry.total_mod[skill_level]:.0%} "
              f"({skill_entry.hit_count[skill_level]} hits)")
        print()


def print_sup_data_entry(chara_data, skill_data, skill_entry, max_level):
    print(f"# Supportive effects - Conditions: {skill_entry.condition_comp.conditions_sorted}")
    print()

    for skill_level in range(max_level):
        skill_level_actual = skill_level + 1

        buff_units = skill_entry.buffs[skill_level]

        print(f"Lv.{skill_level_actual} {'(max)' if max_level == skill_level else ''}")
        print()
        print(f"SP: {skill_data.skill_data_raw.get_sp_at_level(skill_level_actual)}")
        if chara_data.ss_skill_id == skill_data.skill_data_raw.id:
            print(f"SS SP: {skill_data.skill_data_raw.get_ss_sp_at_level(skill_level_actual)}")
        print()

        for buff_unit in buff_units:
            print(f"{buff_unit.target} - {buff_unit.parameter} {buff_unit.rate}")
            if buff_unit.duration_time:
                print(f"Duration: {buff_unit.duration_time} secs")
            if buff_unit.duration_count:
                print(f"{buff_unit.duration_count} stacks (max {buff_unit.max_stack_count})")
            print()


def print_skill_id_entry(chara_data, skill_id_entry):
    skill_id = skill_id_entry.skill_id

    skill_data_sys = _asset_manager.asset_skill.get_data_by_id(skill_id)
    skill_name = _asset_manager.asset_text.to_text(skill_data_sys.name_label)

    print(f"{skill_id_entry.skill_identifier}: {skill_name} ({skill_id})")
    print("-" * 50)

    try:
        data_atk = _asset_manager.transformer_skill.transform_attacking(
            skill_id,
            max_lv=chara_data.max_skill_level(skill_id_entry.skill_num)
        )

        for skill_entry in data_atk.get_all_possible_entries():
            print_atk_data_entry(chara_data, data_atk, skill_entry)
    except Exception as ex:
        print(f"--- No attacking data available for the skill --- {ex}")
        print()

    try:
        data_sup = _asset_manager.transformer_skill.transform_supportive(
            skill_id,
            max_lv=chara_data.max_skill_level(skill_id_entry.skill_num)
        )

        for skill_entry in data_sup.get_all_possible_entries():
            print_sup_data_entry(chara_data, data_sup, skill_entry, data_sup.max_level)
    except Exception as ex:
        print(f"--- No supportive data available for the skill --- {ex}")


def chara_skill_overview(chara_id):
    chara_data = _asset_manager.asset_chara_data.get_data_by_id(chara_id)

    print(f"{chara_data.get_chara_name(_asset_manager.asset_text)} ({chara_id})")
    print("=" * 50)

    for skill_id_entry in chara_data.get_skill_identifiers(_asset_manager):
        print_skill_id_entry(chara_data, skill_id_entry)
        print("=" * 50)


if __name__ == '__main__':
    chara_skill_overview(10450301)
