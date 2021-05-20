from dlparse.enums import Element
from dlparse.transformer import InfoTransformer


def test_not_found(transformer_info: InfoTransformer):
    chara_info = transformer_info.transform_dragon_info(0)

    assert chara_info is None


def test_gala_mars(transformer_info: InfoTransformer):
    # 20050113 - Gala Mars
    dragon_info = transformer_info.transform_dragon_info(20050113)

    assert dragon_info.unit_id == 20050113
    assert dragon_info.name_labels == ["DRAGON_NAME_COMMENT_20050113", "DRAGON_NAME_20050113"]
    assert dragon_info.element == Element.FLAME
    assert dragon_info.rarity == 5
    assert dragon_info.cv_jp_label == "DRAGON_ACTOR_20050113"
    assert dragon_info.cv_en_label == "DRAGON_ACTOR_EN_20050113"


def test_gala_reborn_jeanne(transformer_info: InfoTransformer):
    # 20050414 - Gala Reborn Jeanne
    dragon_info = transformer_info.transform_dragon_info(20050414)

    assert dragon_info.unit_id == 20050414
    assert dragon_info.name_labels == ["DRAGON_NAME_COMMENT_20050414", "DRAGON_NAME_20050414"]
    assert dragon_info.element == Element.LIGHT
    assert dragon_info.rarity == 5
    assert dragon_info.cv_jp_label == "DRAGON_ACTOR_20050414"
    assert dragon_info.cv_en_label == "DRAGON_ACTOR_EN_20050414"


def test_og_sakuya(transformer_info: InfoTransformer):
    # 20050107 - Konohana Sakuya
    dragon_info = transformer_info.transform_dragon_info(20050107)

    assert dragon_info.unit_id == 20050107
    assert dragon_info.name_labels == ["DRAGON_NAME_COMMENT_20050107", "DRAGON_NAME_20050107"]
    assert dragon_info.element == Element.FLAME
    assert dragon_info.rarity == 5
    assert dragon_info.cv_jp_label == "DRAGON_ACTOR_20050107"
    assert dragon_info.cv_en_label == "DRAGON_ACTOR_EN_20050107"


def test_brunhilda(transformer_info: InfoTransformer):
    # 20040101 - Brunhilda
    dragon_info = transformer_info.transform_dragon_info(20040101)

    assert dragon_info.unit_id == 20040101
    assert dragon_info.name_labels == ["DRAGON_NAME_COMMENT_20040101", "DRAGON_NAME_20040101"]
    assert dragon_info.element == Element.FLAME
    assert dragon_info.rarity == 4
    assert dragon_info.cv_jp_label == "DRAGON_ACTOR_20040101"
    assert dragon_info.cv_en_label == "DRAGON_ACTOR_EN_20040101"
