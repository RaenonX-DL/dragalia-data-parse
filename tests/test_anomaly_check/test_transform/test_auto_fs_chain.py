import pytest

from dlparse.enums import Language
from dlparse.export import export_normal_attack_info_as_entry_dict
from dlparse.mono.manager import AssetManager

ALLOWED_EMPTY_AUTO_CHAIN = {
    (10750204, "Unique Dragon"),
}


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
            if (
                    not entry.chain_branches
                    and (unit_id, entry.chain_name.text_dict[Language.EN]) not in ALLOWED_EMPTY_AUTO_CHAIN
            ):
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
