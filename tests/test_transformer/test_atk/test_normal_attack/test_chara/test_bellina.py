import pytest

from dlparse.transformer import AttackingActionTransformer


def test_dragondrive(transformer_atk: AttackingActionTransformer):
    # Bellina (10350503)
    # - Mode 12: Unique Transform
    # - Unique Combo 12
    # - Action ID 300300
    data = transformer_atk.transform_normal_attack_or_fs(300300).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([2.27])
    assert combo_1.sp_gain == 290
    assert combo_1.utp_gain == 180
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([2.72])
    assert combo_2.sp_gain == 350
    assert combo_2.utp_gain == 180
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([4.08])
    assert combo_3.sp_gain == 520
    assert combo_3.utp_gain == 240
    assert combo_3.od_rate == [1.0]
