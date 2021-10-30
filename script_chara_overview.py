from dlparse.enums import Language
from dlparse.errors import HitDataUnavailableError
from dlparse.mono.manager import AssetManager
from tests.static import PATH_LOCAL_ROOT_RESOURCES

_asset_manager: AssetManager = AssetManager(PATH_LOCAL_ROOT_RESOURCES)


def print_atk_data_entry(chara_data, skill_data, skill_entry):
    skill_level = skill_entry.max_level - 1
    skill_level_prev = skill_level - 1

    current_mod = skill_entry.total_mod[skill_level]
    prev_mod = skill_entry.total_mod[skill_level_prev]

    inc_pct = (current_mod / prev_mod) - 1 if prev_mod else 1
    inc_val = current_mod - prev_mod

    cancel_actions = [
        (cancel_unit.action, cancel_unit.time)
        for cancel_unit in skill_entry.cancel_unit_mtx[skill_level]
    ]

    print(f"# Attacking effects (Lv.{skill_entry.max_level}) - "
          f"Conditions: {skill_entry.condition_comp.conditions_sorted}")
    print()
    sp_str = f"SP: {skill_data.skill_data.get_sp_at_level(skill_level)}"
    if chara_data.ss_skill_id == skill_data.skill_data.id:
        sp_str += f" / SS SP: {skill_data.skill_data.get_ss_sp_at_level(skill_level)}"
    print(sp_str)
    print(f"Mods distribution: {skill_entry.mods[skill_level]}")
    print(f"Hit timings (s): {skill_entry.hit_timings[skill_level]}")
    print(f"Cancel actions: {cancel_actions or '(not cancellable)'}")
    print(f"Total Mods: {skill_entry.total_mod[skill_level]:.0%} "
          f"({inc_val:+.0%}, {skill_entry.hit_count[skill_level]} hits) - {inc_pct:+.2%}")
    print()

    afflictions_lv = skill_entry.afflictions[skill_level]
    if afflictions_lv:
        for affliction in afflictions_lv:
            print(f"{affliction.status.name} @ {affliction.time:.3f} s "
                  f"(Rate: {affliction.probability_pct} % |"
                  f" Duration: {affliction.duration_sec} secs)")
        print()

    debuffs_lv = skill_entry.debuffs[skill_level]
    if debuffs_lv:
        for debuff in debuffs_lv:
            print(f"{debuff.parameter.name} {debuff.rate} @ {debuff.time:.3f} s "
                  f"(Rate: {debuff.probability_pct} % |"
                  f" Duration: {debuff.duration_sec} secs)")
        print()


def print_sup_data_entry(chara_data, skill_data, skill_entry, max_level):
    print(f"# Supportive effects - Conditions: {skill_entry.condition_comp.conditions_sorted}")
    print()

    buff_units = skill_entry.buffs[max_level - 1]

    sp_str = f"SP: {skill_data.skill_data.get_sp_at_level(max_level)}"
    if chara_data.ss_skill_id == skill_data.skill_data.id:
        sp_str += f" / SS SP: {skill_data.skill_data.get_ss_sp_at_level(max_level)}"

    print(f"--- Lv.{max_level} {'(max)' if skill_entry.max_level == max_level else ''}| {sp_str}")
    print()

    for buff_unit in buff_units:
        print(f"{buff_unit.target} - {buff_unit.parameter} {buff_unit.rate}")
        if buff_unit.duration_sec:
            print(f"Duration: {buff_unit.duration_sec} secs")
        if buff_unit.duration_count:
            print(f"{buff_unit.duration_count} stacks (max {buff_unit.max_stack_count})")
    print()


def print_skill_id_entry(chara_data, skill_id_entry):
    skill_id = skill_id_entry.skill_id

    skill_data_sys = _asset_manager.asset_skill_data.get_data_by_id(skill_id)
    skill_name = _asset_manager.asset_text_multi.get_text(Language.JP, skill_data_sys.name_label)

    print(f"{' / '.join(skill_id_entry.skill_identifier_labels)}: {skill_name} ({skill_id})")
    print("-" * 50)

    try:
        data_atk = _asset_manager.transformer_skill.transform_attacking(
            skill_id,
            max_lv=chara_data.max_skill_level(skill_id_entry.skill_num),
            # Getting the highest level of the ability only
            # ability_ids=chara_data.ability_ids_at_max_level
        )

        for skill_entry in data_atk.get_all_possible_entries():
            print_atk_data_entry(chara_data, data_atk, skill_entry)
    except HitDataUnavailableError:
        print(f"--- No attacking data available for this skill ---")
        print()

    try:
        data_sup = _asset_manager.transformer_skill.transform_supportive(
            skill_id,
            max_lv=chara_data.max_skill_level(skill_id_entry.skill_num),
            # Getting the highest level of the ability only
            # ability_ids=chara_data.ability_ids_at_max_level
        )

        for skill_entry in data_sup.get_all_possible_entries():
            print_sup_data_entry(chara_data, data_sup, skill_entry, data_sup.max_level)
    except HitDataUnavailableError:
        print(f"--- No supportive data available for this skill ---")


def print_auto_info(auto_id):
    print(f"Auto ID: {auto_id}")
    info = _asset_manager.transformer_atk.transform_normal_attack_or_fs(auto_id)
    for condition_comp in info.possible_conditions:
        print(f"Condition: {condition_comp}")

        combo_branch = info.with_condition(condition_comp)

        for idx, combo in enumerate(combo_branch, start=1):
            print(f"#{idx}: ({len(combo.mods):2d}) {sum(combo.mods):7.0%} UTP +{combo.utp_gain:3d} {combo.mods}")


def chara_skill_overview(chara_id):
    chara_data = _asset_manager.asset_chara_data.get_data_by_id(chara_id)

    if not chara_data:
        print(f"Chara data with ID {chara_id} not found")
        return

    skill_id_entries = chara_data.get_skill_id_entries(_asset_manager)
    skill_identifiers = [
        id_label for skill_id_entry in skill_id_entries for id_label in skill_id_entry.skill_identifier_labels
    ]

    print(f"{chara_data.get_name(_asset_manager.asset_text_multi)} ({chara_id})")
    print()
    print(f"Skill Identifiers available: {' / '.join(skill_identifiers)}")
    if chara_data.has_unique_dragon:
        print("!" * 10 + " UNIQUE DRAGON " + "!" * 10)
    if chara_data.has_unique_weapon:
        print("-" * 10 + " UNIQUE WEAPON " + "-" * 10)
    if chara_data.has_special_win_face:
        print("-" * 10 + " UNIQUE WIN FACE " + "-" * 10)
    print("=" * 50)

    for skill_id_entry in skill_id_entries:
        print_skill_id_entry(chara_data, skill_id_entry)
        print("=" * 50)

    auto_action_ids = [action_id for _, action_id in chara_data.get_normal_attack_variants(_asset_manager)]
    for auto_id in auto_action_ids:
        print_auto_info(auto_id)


def main():
    # - 10150304 (Mona)
    # - 10350505 (Joker)
    # - 10450404 (Sophie)
    # - 10550104 (Panther)
    chara_skill_overview(10650505)


if __name__ == '__main__':
    main()
