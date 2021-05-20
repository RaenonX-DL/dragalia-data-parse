from dlparse.enums import Element, Weapon
from dlparse.transformer import InfoTransformer


def test_not_found(transformer_info: InfoTransformer):
    chara_info = transformer_info.transform_chara_info(0)

    assert chara_info is None


def test_marth(transformer_info: InfoTransformer):
    # 10150102 - Marth
    chara_info = transformer_info.transform_chara_info(10150102)

    assert chara_info.unit_id == 10150102
    assert chara_info.name_labels == ["CHARA_NAME_COMMENT_10150102", "CHARA_NAME_10150102"]
    assert chara_info.element == Element.FLAME
    assert chara_info.rarity == 5
    assert chara_info.weapon_type == Weapon.SWD
    assert not chara_info.has_unique_dragon
    assert chara_info.cv_jp_label == "CHARA_ACTOR_10150102"
    assert chara_info.cv_en_label == "CHARA_ACTOR_EN_10150102"


def test_wedding_elisanne(transformer_info: InfoTransformer):
    # 10150302 - Wedding Elisanne
    chara_info = transformer_info.transform_chara_info(10150302)

    assert chara_info.unit_id == 10150302
    assert chara_info.name_labels == ["CHARA_NAME_COMMENT_10150302", "CHARA_NAME_10150302"]
    assert chara_info.element == Element.WIND
    assert chara_info.rarity == 5
    assert chara_info.weapon_type == Weapon.SWD
    assert not chara_info.has_unique_dragon
    assert chara_info.cv_jp_label == "CHARA_ACTOR_10150302"
    assert chara_info.cv_en_label == "CHARA_ACTOR_EN_10150302"


def test_karina(transformer_info: InfoTransformer):
    # 10440201 - Karina
    chara_info = transformer_info.transform_chara_info(10440201)

    assert chara_info.unit_id == 10440201
    assert chara_info.name_labels == ["CHARA_NAME_COMMENT_10440201", "CHARA_NAME_10440201"]
    assert chara_info.element == Element.WATER
    assert chara_info.rarity == 4
    assert chara_info.weapon_type == Weapon.AXE
    assert not chara_info.has_unique_dragon
    assert chara_info.cv_jp_label == "CHARA_ACTOR_10440201"
    assert chara_info.cv_en_label == "CHARA_ACTOR_EN_10440201"


def test_tiki(transformer_info: InfoTransformer):
    # 10350203 - Tiki
    chara_info = transformer_info.transform_chara_info(10350203)

    assert chara_info.unit_id == 10350203
    assert chara_info.name_labels == ["CHARA_NAME_COMMENT_10350203", "CHARA_NAME_10350203"]
    assert chara_info.element == Element.WATER
    assert chara_info.rarity == 5
    assert chara_info.weapon_type == Weapon.DAG
    assert chara_info.has_unique_dragon
    assert chara_info.cv_jp_label == "CHARA_ACTOR_10350203"
    assert chara_info.cv_en_label == "CHARA_ACTOR_EN_10350203"
