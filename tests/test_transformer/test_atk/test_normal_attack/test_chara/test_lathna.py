import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.export.funcs.normal_attack import export_normal_attack_info_chara
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AttackingActionTransformer


def test_unique_dragon(asset_manager: AssetManager, transformer_atk: AttackingActionTransformer):
    # Lathna (10550502)
    # - Unique Dragon ID 29900004
    # - Action ID 10071140
    ability_ids = asset_manager.asset_chara_data.get_data_by_id(10550502).ability_ids_all_level
    data = transformer_atk.transform_normal_attack_or_fs(10071140, ability_ids=ability_ids).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([2.10])
    assert combo_1.sp_gain == 5
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([2.31])
    assert combo_2.sp_gain == 5
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([1.47] * 2)
    assert combo_3.sp_gain == 5
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2


def test_unique_dragon_enhanced(asset_manager: AssetManager, transformer_atk: AttackingActionTransformer):
    # Lathna (10550502)
    # - Unique Dragon ID 29900004
    # - Action ID 10071140
    ability_ids = asset_manager.asset_chara_data.get_data_by_id(10550502).ability_ids_all_level
    conditions = ConditionComposite(Condition.SELF_PASSIVE_ENHANCED)
    data = transformer_atk.transform_normal_attack_or_fs(10071140, ability_ids=ability_ids).with_condition(conditions)

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([2.31])
    assert combo_1.sp_gain == 5
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([2.54])
    assert combo_2.sp_gain == 5
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([1.67] * 2)
    assert combo_3.sp_gain == 5
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2


def test_export_unique_dragon(asset_manager: AssetManager):
    chara_data = asset_manager.asset_chara_data.get_data_by_id(10550502)
    entries, _ = export_normal_attack_info_chara(chara_data, asset_manager, skip_unparsable=False)

    # 2nd entry is the unique dragon
    # 1 for normal, 1 for enhanced
    assert len(entries[1].chain_branches) == 2
