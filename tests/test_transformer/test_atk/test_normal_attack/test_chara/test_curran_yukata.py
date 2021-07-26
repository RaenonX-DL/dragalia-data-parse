import pytest

from dlparse.export.funcs.normal_attack import export_normal_attack_info_chara
from dlparse.mono.manager import AssetManager


def test_normal_attack_chain(asset_manager: AssetManager):
    # Yukata Curran (10350404)
    # - Uses dagger normal attack despite modes available
    chains, skipped = export_normal_attack_info_chara(
        asset_manager.asset_chara_data.get_data_by_id(10350404),
        asset_manager, skip_unparsable=False
    )

    if skipped:
        pytest.fail(f"Skipped message available: {skipped}")

    if not chains:
        pytest.fail("No chain available.")

    chain = chains[0]

    if not chain.chain_branches:
        pytest.fail("Chain branch unavailable.")
