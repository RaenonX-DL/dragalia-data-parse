import pytest

from dlparse.export.funcs.normal_attack import export_normal_attack_info_chara
from dlparse.mono.manager import AssetManager


def test_normal_attack_chain(asset_manager: AssetManager):
    # Farren (10350405)
    # - Mode 113: Unique Transform
    # - Unique Combo 71
    # - Action ID 301800
    chains, skipped = export_normal_attack_info_chara(
        asset_manager.asset_chara_data.get_data_by_id(10350405),
        asset_manager, skip_unparsable=False
    )

    if skipped:
        pytest.fail(f"Skipped message available: {skipped}")

    if not chains:
        pytest.fail("No chain available.")

    assert len(chains) == 2  # 1 for normal, 1 for enhanced

    if not all(chain.chain_branches for chain in chains):
        pytest.fail("Chain branch unavailable.")
