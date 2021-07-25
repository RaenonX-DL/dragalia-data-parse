"""Functions for exporting normal attack info."""
from typing import Iterable, TYPE_CHECKING

from dlparse.errors import AppValueError, MissingTextError
from dlparse.export.entry import AutoFsChain, AutoFsChainEntry
from .base import export_each_chara_entries, export_each_dragon_entries, export_to_dir

if TYPE_CHECKING:
    from dlparse.mono.asset import CharaDataEntry, DragonDataEntry
    from dlparse.mono.manager import AssetManager

__all__ = (
    "export_auto_fs_info_chara",
    "export_auto_fs_info_as_json", "export_auto_fs_info_as_entry_dict"
)


def export_auto_fs_from_mode_combo_id_pair(
        asset_manager: "AssetManager", mode_combo_ids: Iterable[tuple[int, int]], /,
        skip_unparsable: bool, has_lv_2: bool
):
    """
    Get the combo chains from ``mode_combo_ids``.

    The 1st element of an entry in ``mode_combo_ids`` should be the mode ID;
    the 2nd element of an entry in ``mode_combo_ids`` should be the combo action ID.

    The 2nd element of the return is the missing text labels, if any.
    """
    entries = []
    missing_labels = set()

    for source_mode_id, root_combo_action_id in mode_combo_ids:
        normal_attack_chain = asset_manager.transformer_atk.transform_normal_attack_or_fs(
            root_combo_action_id, 2 if has_lv_2 else None
        )

        try:
            entries.append(AutoFsChainEntry(asset_manager, source_mode_id, normal_attack_chain))
        except MissingTextError as ex:
            if not skip_unparsable:
                raise ex

            missing_labels.update(ex.labels)

    return entries, missing_labels


def export_auto_fs_info_chara(
        chara_data: "CharaDataEntry", asset_manager: "AssetManager",
        skip_unparsable: bool,
) -> tuple[list[AutoFsChain], list[str]]:
    """Get all auto/FS chain info of a character."""
    missing_labels = set()

    normal_entries, normal_missing = export_auto_fs_from_mode_combo_id_pair(
        asset_manager, chara_data.get_normal_attack_variants(asset_manager),
        skip_unparsable=skip_unparsable, has_lv_2=chara_data.is_70_mc
    )
    fs_entries, fs_missing = export_auto_fs_from_mode_combo_id_pair(
        asset_manager, chara_data.get_normal_attack_variants(asset_manager),
        skip_unparsable=skip_unparsable, has_lv_2=chara_data.is_70_mc
    )

    missing_labels.update(normal_missing)
    missing_labels.update(fs_missing)

    chain = AutoFsChain(asset_manager=asset_manager, normal_chains=normal_entries, fs_chains=fs_entries)
    return [chain], list(missing_labels)


def export_auto_fs_info_dragon(
        dragon: "DragonDataEntry", asset_manager: "AssetManager",
        skip_unparsable: bool
) -> tuple[list[AutoFsChain], list[str]]:
    """Get all special auto/FS chain info of a dragon."""
    normal_attack_chain = asset_manager.transformer_atk.transform_normal_attack_or_fs(dragon.normal_attack_action_id)

    try:
        return [AutoFsChain(
            asset_manager=asset_manager,
            normal_chains=[AutoFsChainEntry(asset_manager, 0, normal_attack_chain)],
            fs_chains=[]
        )], []
    except MissingTextError as ex:
        if not skip_unparsable:
            raise ex

        return [], ex.labels


def export_auto_fs_info_as_entry_dict(
        asset_manager: "AssetManager", /,
        skip_unparsable: bool = True,
) -> dict[int, AutoFsChain]:
    """Export special auto/FS chain of all characters and dragons."""
    each = {}
    # Export character normal attack info
    each.update(export_each_chara_entries(
        export_auto_fs_info_chara, asset_manager,
        skip_unparsable=skip_unparsable,
    ))
    # Export dragon normal attack info
    each.update(export_each_dragon_entries(
        export_auto_fs_info_dragon, asset_manager,
        skip_unparsable=skip_unparsable
    ))

    ret = {}
    for unit_id, entries in each.items():
        if len(entries) > 1:
            raise AppValueError(f"Unit #{unit_id} has 1+ chain data where it should only have exactly 1.")

        ret[unit_id] = entries[0]

    return ret


def export_auto_fs_info_as_json(file_dir: str, asset_manager: "AssetManager", /, skip_unparsable: bool = True):
    """Export auto/FS chain info of all characters and dragons as json to ``file_dir``."""
    entries = export_auto_fs_info_as_entry_dict(asset_manager, skip_unparsable=skip_unparsable)
    export_to_dir(entries, file_dir)
