import pytest

from dlparse.transformer import AttackingActionTransformer


def test_normal_ranged(transformer_atk: AttackingActionTransformer):
    # Basileus (10750304)
    # - Action ID 701400
    data = transformer_atk.transform_normal_attack_or_fs(701400).with_condition()

    assert len(data) == 5

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([0.83] * 1 + [0.15] * 2)
    assert combo_1.sp_gain == 130

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([mod for mod in [0.42] + [0.15] * 2] * 2)
    assert combo_2.sp_gain == 200

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([mod for mod in [0.35] + [0.15] * 2] * 3)
    assert combo_3.sp_gain == 240

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([mod for mod in [0.79] + [0.15] * 2] * 2)
    assert combo_4.sp_gain == 430

    combo_5 = data[4]
    assert combo_5.mods == pytest.approx([mod for mod in [0.71] + [0.15] * 3] * 3)
    assert combo_5.sp_gain == 600
