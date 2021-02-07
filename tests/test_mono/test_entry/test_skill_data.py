from dlparse.mono.asset import SkillDataEntry


def create_dummy(**kwargs) -> SkillDataEntry:
    params = {
        "id": 0,
        "name_label": "",
        "skill_type_id": 0,
        "icon_lv1_label": "",
        "icon_lv2_label": "",
        "icon_lv3_label": "",
        "icon_lv4_label": "",
        "description_lv1_label": "",
        "description_lv2_label": "",
        "description_lv3_label": "",
        "description_lv4_label": "",
        "sp_lv1": 0,
        "sp_lv2": 0,
        "sp_lv3": 0,
        "sp_lv4": 0,
        "sp_ss_lv1": 0,
        "sp_ss_lv2": 0,
        "sp_ss_lv3": 0,
        "sp_ss_lv4": 0,
        "sp_dragon_lv1": 0,
        "sp_dragon_lv2": 0,
        "sp_dragon_lv3": 0,
        "sp_dragon_lv4": 0,
        "sp_gauge_count": 0,
        "required_buff_id": 0,
        "required_buff_count": 0,
        "action_1_id": 0,
        "action_2_id": 0,
        "action_3_id": 0,
        "action_4_id": 0,
        "adv_skill_lv1": 0,
        "adv_skill_lv1_action_id": 0,
        "ability_lv1_id": 0,
        "ability_lv2_id": 0,
        "ability_lv3_id": 0,
        "ability_lv4_id": 0,
        "chain_group_id": 0,
        "trans_skill_id": 0,
        "trans_condition_id": 0,
        "trans_hit_count": 0,
        "trans_text_label": "",
        "trans_time": 0.0,
        "trans_action_id": 0,
        "max_use_count": 0,
        "mode_change_skill_id": 0,
        "as_helper_skill_id": 0,
        "is_affected_by_tension_lv1": False,
        "is_affected_by_tension_lv2": False,
        "is_affected_by_tension_lv3": False,
        "is_affected_by_tension_lv4": False,
    }

    params.update(kwargs)

    return SkillDataEntry(**params)


def test_action_id_by_level_action_1_only():
    entry = create_dummy(action_1_id=1, ability_lv3_id=3, ability_lv4_id=4)

    assert entry.get_action_id_by_level() == [
        (1, 1, 1),
        (1, 2, 1),
        (1, 3, 1),
        (1, 4, 1),
    ]


def test_action_id_by_level_action_1_only_adv_at_3():
    entry = create_dummy(
        action_1_id=1, adv_skill_lv1=3, adv_skill_lv1_action_id=3, ability_lv3_id=3, ability_lv4_id=4
    )

    assert entry.get_action_id_by_level() == [
        (1, 1, 1),
        (1, 2, 1),
        (3, 3, 1),
        (3, 4, 1),
    ]


def test_action_id_by_level_action_1_only_adv_at_4():
    entry = create_dummy(
        action_1_id=1, adv_skill_lv1=4, adv_skill_lv1_action_id=3, ability_lv3_id=3, ability_lv4_id=4
    )

    assert entry.get_action_id_by_level() == [
        (1, 1, 1),
        (1, 2, 1),
        (1, 3, 1),
        (3, 4, 1),
    ]


def test_action_id_by_level_split_2():
    entry = create_dummy(action_1_id=1, action_2_id=2, ability_lv3_id=3, ability_lv4_id=4)

    assert entry.get_action_id_by_level() == [
        (1, 1, 1 / 2),
        (2, 1, 1 / 2),
        (1, 2, 1 / 2),
        (2, 2, 1 / 2),
        (1, 3, 1 / 2),
        (2, 3, 1 / 2),
        (1, 4, 1 / 2),
        (2, 4, 1 / 2),
    ]


def test_action_id_by_level_split_2_adv_at_3():
    entry = create_dummy(
        action_1_id=1, action_2_id=2, adv_skill_lv1=3, adv_skill_lv1_action_id=5, ability_lv3_id=3, ability_lv4_id=4
    )

    assert entry.get_action_id_by_level() == [
        (1, 1, 1 / 2),
        (2, 1, 1 / 2),
        (1, 2, 1 / 2),
        (2, 2, 1 / 2),
        (5, 3, 1),
        (5, 4, 1),
    ]


def test_action_id_by_level_split_2_adv_at_4():
    entry = create_dummy(
        action_1_id=1, action_2_id=2, ability_lv3_id=3, ability_lv4_id=4, adv_skill_lv1=4, adv_skill_lv1_action_id=5
    )

    assert entry.get_action_id_by_level() == [
        (1, 1, 1 / 2),
        (2, 1, 1 / 2),
        (1, 2, 1 / 2),
        (2, 2, 1 / 2),
        (1, 3, 1 / 2),
        (2, 3, 1 / 2),
        (5, 4, 1),
    ]


def test_action_id_by_level_split_3():
    entry = create_dummy(
        action_1_id=1, action_2_id=2, action_3_id=8, ability_lv3_id=3, ability_lv4_id=4
    )

    assert entry.get_action_id_by_level() == [
        (1, 1, 1 / 3),
        (2, 1, 1 / 3),
        (8, 1, 1 / 3),
        (1, 2, 1 / 3),
        (2, 2, 1 / 3),
        (8, 2, 1 / 3),
        (1, 3, 1 / 3),
        (2, 3, 1 / 3),
        (8, 3, 1 / 3),
        (1, 4, 1 / 3),
        (2, 4, 1 / 3),
        (8, 4, 1 / 3),
    ]


def test_action_id_by_level_split_4():
    entry = create_dummy(
        action_1_id=1, action_2_id=2, action_3_id=8, action_4_id=9, ability_lv3_id=3, ability_lv4_id=4
    )

    assert entry.get_action_id_by_level() == [
        (1, 1, 1 / 4),
        (2, 1, 1 / 4),
        (8, 1, 1 / 4),
        (9, 1, 1 / 4),
        (1, 2, 1 / 4),
        (2, 2, 1 / 4),
        (8, 2, 1 / 4),
        (9, 2, 1 / 4),
        (1, 3, 1 / 4),
        (2, 3, 1 / 4),
        (8, 3, 1 / 4),
        (9, 3, 1 / 4),
        (1, 4, 1 / 4),
        (2, 4, 1 / 4),
        (8, 4, 1 / 4),
        (9, 4, 1 / 4),
    ]


def test_action_id_by_level_split_4_adv_at_3():
    entry = create_dummy(
        action_1_id=1, action_2_id=2, action_3_id=8, action_4_id=9,
        adv_skill_lv1=3, adv_skill_lv1_action_id=5, ability_lv3_id=3, ability_lv4_id=4
    )

    assert entry.get_action_id_by_level() == [
        (1, 1, 1 / 4),
        (2, 1, 1 / 4),
        (8, 1, 1 / 4),
        (9, 1, 1 / 4),
        (1, 2, 1 / 4),
        (2, 2, 1 / 4),
        (8, 2, 1 / 4),
        (9, 2, 1 / 4),
        (5, 3, 1),
        (5, 4, 1),
    ]
