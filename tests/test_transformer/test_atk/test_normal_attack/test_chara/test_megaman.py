import pytest

from dlparse.export.funcs.normal_attack import export_normal_attack_info_chara
from dlparse.mono.manager import AssetManager


def test_s2_effective_chain(asset_manager: AssetManager):
    # Megaman (10750102)
    chains, skipped = export_normal_attack_info_chara(
        asset_manager.asset_chara_data.get_data_by_id(10750102),
        asset_manager, skip_unparsable=False
    )

    if skipped:
        pytest.fail(f"Skipped message available: {skipped}")

    if not chains:
        pytest.fail("No chain available.")

    # Chain for S2 effective
    chain = chains[2]

    if not chain.chain_branches:
        pytest.fail("Chain branch unavailable.")
