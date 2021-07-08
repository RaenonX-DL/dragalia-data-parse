"""Functions for exporting normal attack info."""
import os.path
from typing import TYPE_CHECKING

from dlparse.errors import MissingTextError
from dlparse.export.entry import NormalAttackChainEntry
from .base import export_as_json, export_each_chara_entries

if TYPE_CHECKING:
    from dlparse.mono.asset import CharaDataEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("export_normal_attack_info_as_json", "export_normal_attack_info_as_entry_dict")


def export_normal_attack_info_chara(
        chara_data: "CharaDataEntry", asset_manager: "AssetManager",
        _: bool, __: bool
) -> tuple[list[NormalAttackChainEntry], list[str]]:
    """Get all special normal attack chain info of a character."""
    chain_entries = []
    missing_labels = set()

    for source_mode_id, root_combo_action_id in chara_data.get_normal_attack_variants(asset_manager):
        normal_attack_chain = asset_manager.transformer_atk.transform_normal_attack(
            root_combo_action_id, 2 if chara_data.is_70_mc else None
        )

        try:
            chain_entries.append(NormalAttackChainEntry(asset_manager, source_mode_id, normal_attack_chain))
        except MissingTextError as ex:
            missing_labels.update(ex.labels)

    return chain_entries, list(missing_labels)


def export_normal_attack_info_as_entry_dict(
        asset_manager: "AssetManager", /,
        skip_unparsable: bool = True,
) -> dict[int, list[NormalAttackChainEntry]]:
    """Export special normal attack chain of a character."""
    return export_each_chara_entries(
        export_normal_attack_info_chara, asset_manager,
        skip_unparsable=skip_unparsable, include_dragon=False,
    )


def export_normal_attack_info_as_json(file_dir: str, asset_manager: "AssetManager", /, skip_unparsable: bool = True):
    """Export normal attack info of all characters and dragons as json to ``file_dir``."""
    entries = export_normal_attack_info_as_entry_dict(asset_manager, skip_unparsable=skip_unparsable)
    for unit_id, info_entries in entries.items():
        export_as_json(info_entries, os.path.join(file_dir, f"{unit_id}.json"))
