"""Functions for exporting normal attack info."""
from typing import TYPE_CHECKING

from dlparse.errors import MissingTextError
from dlparse.export.entry import NormalAttackChainEntry
from .base import export_each_chara_entries, export_each_dragon_entries, export_to_dir

if TYPE_CHECKING:
    from dlparse.mono.asset import CharaDataEntry, DragonDataEntry
    from dlparse.mono.manager import AssetManager

__all__ = (
    "export_normal_attack_info_chara",
    "export_normal_attack_info_as_json", "export_normal_attack_info_as_entry_dict"
)


def export_normal_attack_info_chara(
        chara_data: "CharaDataEntry", asset_manager: "AssetManager",
        skip_unparsable: bool,
) -> tuple[list[NormalAttackChainEntry], list[str]]:
    """Get all special normal attack chain info of a character."""
    chain_entries = []
    missing_labels = set()

    for source_mode_id, root_combo_action_id in chara_data.get_normal_attack_variants(asset_manager):
        normal_attack_chain = asset_manager.transformer_atk.transform_normal_attack_or_fs(
            root_combo_action_id, 2 if chara_data.is_70_mc and source_mode_id != -1 else None,
            ability_ids=chara_data.ability_ids_all_level
        )

        try:
            chain_entries.append(NormalAttackChainEntry(asset_manager, source_mode_id, normal_attack_chain))
        except MissingTextError as ex:
            if not skip_unparsable:
                raise ex

            missing_labels.update(ex.labels)

    return chain_entries, list(missing_labels)


def export_normal_attack_info_dragon(
        dragon: "DragonDataEntry", asset_manager: "AssetManager",
        skip_unparsable: bool
) -> tuple[list[NormalAttackChainEntry], list[str]]:
    """Get all special normal attack chain info of a dragon."""
    normal_attack_chain = asset_manager.transformer_atk.transform_normal_attack_or_fs(dragon.normal_attack_action_id)

    try:
        return [NormalAttackChainEntry(asset_manager, 0, normal_attack_chain)], []
    except MissingTextError as ex:
        if not skip_unparsable:
            raise ex

        return [], ex.labels


def export_normal_attack_info_as_entry_dict(
        asset_manager: "AssetManager", /,
        skip_unparsable: bool = True,
) -> dict[int, list[NormalAttackChainEntry]]:
    """Export special normal attack chain of all characters and dragons."""
    ret = {}
    # Export character normal attack info
    ret.update(export_each_chara_entries(
        export_normal_attack_info_chara, asset_manager,
        skip_unparsable=skip_unparsable,
    ))
    # Export dragon normal attack info
    ret.update(export_each_dragon_entries(
        export_normal_attack_info_dragon, asset_manager,
        skip_unparsable=skip_unparsable
    ))
    return ret


def export_normal_attack_info_as_json(file_dir: str, asset_manager: "AssetManager", /, skip_unparsable: bool = True):
    """Export normal attack info of all characters and dragons as json to ``file_dir``."""
    entries = export_normal_attack_info_as_entry_dict(asset_manager, skip_unparsable=skip_unparsable)
    export_to_dir(entries, file_dir)
