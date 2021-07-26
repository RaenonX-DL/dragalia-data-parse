import pytest

from dlparse.export import export_normal_attack_info_as_entry_dict
from dlparse.mono.manager import AssetManager


@pytest.mark.holistic
def test_no_empty_auto_chain(asset_manager: AssetManager):
    entry_dict = export_normal_attack_info_as_entry_dict(asset_manager)

    unit_ids_empty_chain = []
    unit_ids_empty_chain_branch = []

    for unit_id, entries in entry_dict.items():
        if not entries:
            unit_ids_empty_chain.append(unit_id)
            continue

        for entry in entries:
            if not entry.chain_branches:
                unit_ids_empty_chain_branch.append(unit_id)
                continue

    if unit_ids_empty_chain or unit_ids_empty_chain_branch:
        message = ""

        if unit_ids_empty_chain:
            message += "\nSome units have empty chain:\n"
            message += "\n".join([f"- {unit_entry}" for unit_entry in unit_ids_empty_chain])

        if unit_ids_empty_chain_branch:
            message += "\nSome units have empty chain branch:\n"
            message += "\n".join([f"- {unit_entry}" for unit_entry in unit_ids_empty_chain_branch])

        pytest.fail(message)
