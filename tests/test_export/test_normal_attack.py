import pytest

from dlparse.enums import Language
from dlparse.export import export_normal_attack_info_as_entry_dict
from dlparse.export.entry import NormalAttackChainEntry
from dlparse.export.funcs.normal_attack import export_normal_attack_info_chara
from dlparse.mono.manager import AssetManager
from tests.utils import is_json_schema_match


@pytest.mark.holistic
def test_exported_json(asset_manager: AssetManager):
    entry_dict = export_normal_attack_info_as_entry_dict(asset_manager)

    for entries in entry_dict.values():
        for entry in entries:
            is_json_schema_match(NormalAttackChainEntry.json_schema, entry.to_json_entry())


def test_export_unique_dragon_combo_chain(asset_manager: AssetManager):
    chara_data_tiki = asset_manager.asset_chara_data.get_data_by_id(10350203)
    entries, _ = export_normal_attack_info_chara(chara_data_tiki, asset_manager, skip_unparsable=False)

    chain_names_expected = {
        asset_manager.asset_text_website.get_text(Language.EN, label)
        for label in ("NORMAL_ATTACK_COMBO_CHAIN_0", "NORMAL_ATTACK_COMBO_CHAIN_-1")
    }
    chain_names_actual = {entry.chain_name.text_dict[Language.EN] for entry in entries}

    assert chain_names_expected == chain_names_actual


def test_branched_chain_has_utp_has_crisis(asset_manager: AssetManager):
    # Bellina (10350503)
    # - Mode 12: Unique Transform
    # - Unique Combo 12
    # - Action ID 300300
    chain_data = asset_manager.transformer_atk.transform_normal_attack_or_fs(300300)
    chain_data = NormalAttackChainEntry(asset_manager, 12, chain_data).chain_branches[0]
    assert chain_data.has_utp
    assert chain_data.has_crisis_mods


def test_branched_chain_has_utp_no_crisis(asset_manager: AssetManager):
    # Nino (10150305)
    # - Mode 95: Unique Transform
    # - Unique Combo 67
    # - Action ID 101100
    chain_data = asset_manager.transformer_atk.transform_normal_attack_or_fs(101100)
    chain_data = NormalAttackChainEntry(asset_manager, 95, chain_data).chain_branches[0]
    assert chain_data.has_utp
    assert not chain_data.has_crisis_mods


def test_branched_chain_no_utp_no_crisis(asset_manager: AssetManager):
    # Gala Mascula (10250203)
    # - Mode 93: Normal
    # - Unique Combo 65
    # - Action ID 202700
    chain_data = asset_manager.transformer_atk.transform_normal_attack_or_fs(202700)
    chain_data = NormalAttackChainEntry(asset_manager, 93, chain_data).chain_branches[0]
    assert not chain_data.has_utp
    assert not chain_data.has_crisis_mods
