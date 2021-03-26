import pytest

from dlparse.enums import Element
from dlparse.transformer import EnemyTransformer


def test_lilith_enchroaching_shadow_expert_solo(transformer_enemy: EnemyTransformer):
    # Lilith's Encroaching Shadow (Expert) - Solo
    # https://dl.raenonx.cc/quest/13#pos-4
    enemy_data = transformer_enemy.transform_enemy_data(228051201)

    # Check form count
    assert enemy_data.form_count == 2

    # Check form 1 data
    enemy_data_form_1 = enemy_data.forms[0]

    assert enemy_data_form_1.enemy_param_id == 228051201
    assert enemy_data_form_1.initial_element == Element.SHADOW
    assert enemy_data_form_1.hp == 2540800
    assert enemy_data_form_1.defense == 15

    # Check form 2 data
    enemy_data_form_2 = enemy_data.forms[1]

    assert enemy_data_form_2.enemy_param_id == 228051203
    assert enemy_data_form_2.initial_element == Element.SHADOW
    assert enemy_data_form_2.hp == 7344920
    assert enemy_data_form_2.defense == 15
    assert enemy_data_form_2.base_od == 1468984
    assert enemy_data_form_2.base_bk == 3672460
    assert enemy_data_form_2.od_def_rate == 1.0
    assert enemy_data_form_2.od_atk_rate == 1.2
    assert enemy_data_form_2.bk_def_rate == 0.8
    assert enemy_data_form_2.bk_duration_sec == 10

    expected_parts_id = {228051204, 228051205}
    for part in enemy_data_form_2.parts:
        part_id = part.enemy_param_id
        if part_id not in expected_parts_id:
            pytest.fail(f"Unexpected part ID: {part_id}")

        expected_parts_id.remove(part_id)
        assert part.hp == 1468984
        assert part.defense == 10
    assert len(expected_parts_id) == 0, f"Not all expected parts are returned. Not returned: {expected_parts_id}"


def test_lilith_enchroaching_shadow_master_solo(transformer_enemy: EnemyTransformer):
    # Lilith's Encroaching Shadow (Master) - Solo
    # https://dl.raenonx.cc/quest/13#pos-5
    enemy_data = transformer_enemy.transform_enemy_data(228051301)

    # Check form count
    assert enemy_data.form_count == 1

    # Check form 1 data
    enemy_data_form_1 = enemy_data.forms[0]

    assert enemy_data_form_1.enemy_param_id == 228051301
    assert enemy_data_form_1.initial_element == Element.SHADOW
    assert enemy_data_form_1.hp == 12781024
    assert enemy_data_form_1.defense == 15
    assert enemy_data_form_1.base_od == 2556204
    assert enemy_data_form_1.base_bk == 6390512
    assert enemy_data_form_1.od_def_rate == 1.0
    assert enemy_data_form_1.od_atk_rate == 1.2
    assert enemy_data_form_1.bk_def_rate == 0.8
    assert enemy_data_form_1.bk_duration_sec == 10

    # Check form 1 part

    expected_parts_id = {228051302, 228051303}
    for part in enemy_data_form_1.parts:
        part_id = part.enemy_param_id
        if part_id not in expected_parts_id:
            pytest.fail(f"Unexpected part ID: {part_id}")

        expected_parts_id.remove(part_id)
        assert part.hp == 2556205
        assert part.defense == 10

    assert len(expected_parts_id) == 0, f"Not all expected parts are returned. Not returned: {expected_parts_id}"

    # Check form 1 children

    expected_children_id_hp = {228051304: 9999999, 228051305: 160000}
    expected_children_id_def = {228051304: 15, 228051305: 10}
    for child in enemy_data_form_1.children:
        child_id = child.enemy_param_id
        if child_id not in expected_children_id_hp:
            pytest.fail(f"Unexpected child ID: {child_id}")

        assert child.hp == expected_children_id_hp[child_id]
        assert child.defense == expected_children_id_def[child_id]

        expected_children_id_hp.pop(child_id)

    assert \
        len(expected_children_id_hp) == 0, \
        f"Not all expected children are returned. Not returned: {expected_children_id_hp}"


def test_legend_ciella_solo(transformer_enemy: EnemyTransformer):
    # Legend Ciella - Solo
    enemy_data = transformer_enemy.transform_enemy_data(225031401)

    # Check form count
    assert enemy_data.form_count == 2

    # Check form 1 data
    enemy_data_form_1 = enemy_data.forms[0]

    assert enemy_data_form_1.enemy_param_id == 225031401
    assert enemy_data_form_1.initial_element == Element.WATER
    assert enemy_data_form_1.hp == 6714487
    assert enemy_data_form_1.defense == 10
    assert enemy_data_form_1.od_atk_rate == 1.2

    # Check form 1 children
    expected_children_id_hp = {225031403: 13850, 225031404: 48759, 225031410: 15}
    expected_children_id_def = {225031403: 10, 225031404: 10, 225031410: 10}
    for child in enemy_data_form_1.children:
        child_id = child.enemy_param_id
        if child_id not in expected_children_id_hp:
            pytest.fail(f"Unexpected child ID: {child_id}")

        assert child.hp == expected_children_id_hp[child_id]
        assert child.defense == expected_children_id_def[child_id]

        expected_children_id_hp.pop(child_id)

    assert \
        len(expected_children_id_hp) == 0, \
        f"Not all expected children are returned. Not returned: {expected_children_id_hp}"

    # Check form 2 data
    enemy_data_form_2 = enemy_data.forms[1]

    assert enemy_data_form_2.enemy_param_id == 225031402
    assert enemy_data_form_2.initial_element == Element.WATER
    assert enemy_data_form_2.hp == 22891629
    assert enemy_data_form_2.defense == 10
    assert enemy_data_form_2.base_od == 3433744
    assert enemy_data_form_2.base_bk == 5722907
    assert enemy_data_form_2.od_def_rate == 1.0
    assert enemy_data_form_2.od_atk_rate == 1.2
    assert enemy_data_form_2.bk_def_rate == 0.8
    assert enemy_data_form_2.bk_duration_sec == 10

    # Check form 2 children
    expected_children_id_hp = {225031405: 18500, 225031404: 48759, 225031410: 15}
    expected_children_id_def = {225031405: 10, 225031404: 10, 225031410: 10}
    for child in enemy_data_form_2.children:
        child_id = child.enemy_param_id
        if child_id not in expected_children_id_hp:
            pytest.fail(f"Unexpected child ID: {child_id}")

        assert child.hp == expected_children_id_hp[child_id]
        assert child.defense == expected_children_id_def[child_id]

        expected_children_id_hp.pop(child_id)

    assert \
        len(expected_children_id_hp) == 0, \
        f"Not all expected children are returned. Not returned: {expected_children_id_hp}"


def test_legend_ciella_coop(transformer_enemy: EnemyTransformer):
    # Legend Ciella - Coop
    enemy_data = transformer_enemy.transform_enemy_data(225030401)

    # Check form count
    assert enemy_data.form_count == 2

    # Check form 1 data
    enemy_data_form_1 = enemy_data.forms[0]

    assert enemy_data_form_1.enemy_param_id == 225030401
    assert enemy_data_form_1.initial_element == Element.WATER
    assert enemy_data_form_1.hp == 9728658
    assert enemy_data_form_1.defense == 10
    assert enemy_data_form_1.od_atk_rate == 1.2

    # Check form 1 children
    expected_children_id_hp = {225030403: 37560, 225030404: 48759, 225030410: 70}
    expected_children_id_def = {225030403: 10, 225030404: 10, 225030410: 10}
    for child in enemy_data_form_1.children:
        child_id = child.enemy_param_id
        if child_id not in expected_children_id_hp:
            pytest.fail(f"Unexpected child ID: {child_id}")

        assert child.hp == expected_children_id_hp[child_id]
        assert child.defense == expected_children_id_def[child_id]

        expected_children_id_hp.pop(child_id)

    assert \
        len(expected_children_id_hp) == 0, \
        f"Not all expected children are returned. Not returned: {expected_children_id_hp}"

    # Check form 2 data
    enemy_data_form_2 = enemy_data.forms[1]

    assert enemy_data_form_2.enemy_param_id == 225030402
    assert enemy_data_form_2.initial_element == Element.WATER
    assert enemy_data_form_2.hp == 32688455
    assert enemy_data_form_2.defense == 10
    assert enemy_data_form_2.base_od == 6537691
    assert enemy_data_form_2.base_bk == 8172130
    assert enemy_data_form_2.od_def_rate == 1.0
    assert enemy_data_form_2.od_atk_rate == 1.2
    assert enemy_data_form_2.bk_def_rate == 0.8
    assert enemy_data_form_2.bk_duration_sec == 10

    # Check form 2 children
    expected_children_id_hp = {225030405: 21580, 225030404: 48759, 225030410: 70}
    expected_children_id_def = {225030405: 10, 225030404: 10, 225030410: 10}
    for child in enemy_data_form_2.children:
        child_id = child.enemy_param_id
        if child_id not in expected_children_id_hp:
            pytest.fail(f"Unexpected child ID: {child_id}")

        assert child.hp == expected_children_id_hp[child_id]
        assert child.defense == expected_children_id_def[child_id]

        expected_children_id_hp.pop(child_id)

    assert \
        len(expected_children_id_hp) == 0, \
        f"Not all expected children are returned. Not returned: {expected_children_id_hp}"
