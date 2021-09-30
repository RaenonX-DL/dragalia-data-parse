import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.export.funcs.normal_attack import export_normal_attack_info_chara
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AttackingActionTransformer


def test_normal_attack_chain(asset_manager: AssetManager):
    # Gala Zethia (10250504)
    chains, skipped = export_normal_attack_info_chara(
        asset_manager.asset_chara_data.get_data_by_id(10250504),
        asset_manager, skip_unparsable=False
    )

    if skipped:
        pytest.fail(f"Skipped message available: {skipped}")

    if not chains:
        pytest.fail("No chain available.")

    # Normal, w/ Bahamut, Bahamut's normal
    assert len(chains) == 3

    if any(not chain.chain_branches for chain in chains):
        pytest.fail("Chain branch unavailable.")


def test_normal(transformer_atk: AttackingActionTransformer):
    # Gala Zethia (10250504)
    # - Mode 115: Normal
    # - Unique Combo 72
    # - Action ID 202900
    # - Not summoned
    conditions = ConditionComposite(Condition.MODE_0)
    data = transformer_atk.transform_normal_attack_or_fs(202900).with_condition(conditions)

    assert data[0].mods == pytest.approx([0.59])
    assert data[1].mods == pytest.approx([0.34] * 2)
    assert data[2].mods == pytest.approx([0.49] * 3)
    assert data[3].mods == pytest.approx([0.67] * 5)
    assert data[4].mods == pytest.approx([1.04] * 3)
    assert data[5].mods == pytest.approx([1.14] * 2)
    assert data[6].mods == pytest.approx([0.88] * 3)
    assert data[7].mods == pytest.approx([1.44] * 3)
    assert data[8].mods == pytest.approx([0.95] * 6 + [1.89] * 2)


def test_mode_switched(transformer_atk: AttackingActionTransformer):
    # Gala Zethia (10250504)
    # - Mode 115: Normal
    # - Unique Combo 72
    # - Action ID 202900
    conditions = ConditionComposite(Condition.MODE_1)
    data = transformer_atk.transform_normal_attack_or_fs(202900).with_condition(conditions)

    assert data[0].mods == pytest.approx([0.59])
    assert data[1].mods == pytest.approx([0.34] * 2)
    assert data[2].mods == pytest.approx([0.73] * 3)
    assert data[3].mods == pytest.approx([0.67] * 5)
    assert data[4].mods == pytest.approx([1.55] * 3)
    assert data[5].mods == pytest.approx([1.14] * 2)
    assert data[6].mods == pytest.approx([0.88] * 2 + [1.32])
    assert data[7].mods == pytest.approx([1.44] * 2 + [2.14])
    assert data[8].mods == pytest.approx([0.95] * 6 + [2.84] * 2)
