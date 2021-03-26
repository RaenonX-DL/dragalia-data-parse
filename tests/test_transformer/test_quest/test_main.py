from dlparse.enums import Element, QuestMode
from dlparse.transformer import QuestTransformer


def test_lilith_enchroaching_shadow_expert_solo(transformer_quest: QuestTransformer):
    # Lilith's Encroaching Shadow (Expert) - Solo
    # https://dl.raenonx.cc/quest/13#pos-4
    quest_data = transformer_quest.transform_quest_data(228050102)

    assert quest_data.quest_mode == QuestMode.MULTI
    assert quest_data.elements == [Element.SHADOW]
    assert quest_data.elements_limit == []
    assert quest_data.max_clear_time_sec == 600
    assert quest_data.max_revive_allowed == 1
    assert quest_data.area_1_name == "DIABOLOS_05_0101_01"
    assert quest_data.spawn_enemy_param_ids == [228050201]


def test_lilith_enchroaching_shadow_master_solo(transformer_quest: QuestTransformer):
    # Lilith's Encroaching Shadow (Expert) - Solo
    # https://dl.raenonx.cc/quest/13#pos-4
    quest_data = transformer_quest.transform_quest_data(228051103)

    assert quest_data.quest_mode == QuestMode.SOLO
    assert quest_data.elements == [Element.SHADOW, Element.FLAME]
    assert quest_data.elements_limit == [Element.LIGHT, Element.WATER]
    assert quest_data.max_clear_time_sec == 600
    assert quest_data.max_revive_allowed == 0
    assert quest_data.area_1_name == "DIABOLOS_05_0111_02"
    assert quest_data.spawn_enemy_param_ids == [228051301]


def test_legend_ciella_solo(transformer_quest: QuestTransformer):
    # Legend Ciella - Solo
    quest_data = transformer_quest.transform_quest_data(225031101)

    assert quest_data.quest_mode == QuestMode.SOLO
    assert quest_data.elements == [Element.WATER]
    assert quest_data.elements_limit == [Element.WIND]
    assert quest_data.max_clear_time_sec == 600
    assert quest_data.max_revive_allowed == 0
    assert quest_data.area_1_name == "AGITO_ABS_03_1102_01"
    assert quest_data.spawn_enemy_param_ids == [225031401]


def test_legend_ciella_coop(transformer_quest: QuestTransformer):
    # Legend Ciella - Coop
    quest_data = transformer_quest.transform_quest_data(225030101)

    assert quest_data.quest_mode == QuestMode.MULTI
    assert quest_data.elements == [Element.WATER]
    assert quest_data.elements_limit == [Element.WIND]
    assert quest_data.max_clear_time_sec == 480
    assert quest_data.max_revive_allowed == 0
    assert quest_data.area_1_name == "AGITO_ABS_03_0102_01"
    assert quest_data.spawn_enemy_param_ids == [225030401]
