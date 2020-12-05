from dlparse.mono.asset import SkillDataEntry


def create_dummy(**kwargs) -> SkillDataEntry:
    params = {
        "id": -1,
        "name_label": "",
        "skill_type_id": -1,
        "icon_lv1_label": "",
        "icon_lv2_label": "",
        "icon_lv3_label": "",
        "icon_lv4_label": "",
        "description_lv1_label": "",
        "description_lv2_label": "",
        "description_lv3_label": "",
        "description_lv4_label": "",
        "sp_lv1": -1,
        "sp_lv2": -1,
        "sp_lv3": -1,
        "sp_lv4": -1,
        "sp_ss_lv1": -1,
        "sp_ss_lv2": -1,
        "sp_ss_lv3": -1,
        "sp_ss_lv4": -1,
        "sp_dragon_lv1": -1,
        "sp_dragon_lv2": -1,
        "sp_dragon_lv3": -1,
        "sp_dragon_lv4": -1,
        "sp_gauge_count": -1,
        "required_buff_id": -1,
        "required_buff_count": -1,
        "action_1_id": 0,
        "action_2_id": 0,
        "action_3_id": 0,
        "action_4_id": 0,
        "adv_skill_lv1": 0,
        "adv_skill_lv1_action_id": 0,
        "ability_lv1_id": -1,
        "ability_lv2_id": -1,
        "ability_lv3_id": -1,
        "ability_lv4_id": -1,
        "trans_skill_id": -1,
        "trans_condition_id": -1,
        "trans_hit_count": -1,
        "trans_text_label": "",
        "trans_time": 0.0,
        "trans_action_id": -1,
        "max_use_count": -1,
        "mode_change_skill_id": -1,
        "as_helper_skill_id": -1,
        "is_affected_by_tension_lv1": False,
        "is_affected_by_tension_lv2": False,
        "is_affected_by_tension_lv3": False,
        "is_affected_by_tension_lv4": False,
    }

    params.update(kwargs)

    return SkillDataEntry(**params)


def test_action_id_1_by_level_1():
    entry = create_dummy(action_1_id=1, action_2_id=2, ability_lv3_id=3, ability_lv4_id=4,
                         adv_skill_lv1=3, adv_skill_lv1_action_id=5)

    assert entry.action_id_1_by_level == [1, 1, 5, 5]


def test_action_id_1_by_level_2():
    entry = create_dummy(action_1_id=1, action_2_id=2, ability_lv3_id=3, ability_lv4_id=4)

    assert entry.action_id_1_by_level == [1, 1, 1, 1]


def test_action_id_1_by_level_3():
    entry = create_dummy(action_1_id=1, action_2_id=2, ability_lv3_id=3, ability_lv4_id=4,
                         adv_skill_lv1=4, adv_skill_lv1_action_id=5)

    assert entry.action_id_1_by_level == [1, 1, 1, 5]
