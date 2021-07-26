"""Base exporting functions."""
import csv
import os
from json import JSONEncoder, dump
from typing import Any, Callable, Optional, TypeVar, Union

from dlparse.errors import ActionDataNotFoundError, HitDataUnavailableError, MotionDataNotFoundError
from dlparse.export.entry import CsvExportableEntryBase, JsonExportableEntryBase, SkillExportEntryBase
from dlparse.model import SkillDataBase
from dlparse.mono.asset import CharaDataEntry, DragonDataEntry, SkillIdEntry, UnitEntry
from dlparse.mono.manager import AssetManager

__all__ = (
    "export_as_csv", "export_as_json", "export_to_dir", "print_skipped_messages", "export_transform_skill_entries",
    "export_entries_merged", "export_each_chara_entries", "export_each_dragon_entries",
)

CT = TypeVar("CT", bound=CsvExportableEntryBase)
JT = TypeVar("JT", bound=JsonExportableEntryBase)
ET = TypeVar("ET", bound=SkillExportEntryBase)
DT = TypeVar("DT", bound=SkillDataBase)

CharaEntryParsingFunction = Callable[
    [CharaDataEntry, AssetManager, bool],
    tuple[list[JT], list[str]]
]

DragonEntryParsingFunction = Callable[
    [DragonDataEntry, AssetManager, bool],
    tuple[list[JT], list[str]]
]

UnitEntryParsingFunction = Callable[
    [UnitEntry, AssetManager, bool],
    tuple[list[JT], list[str]]
]

TransformFunction = Callable[
    [int, int, Optional[list[int]]],
    DT
]

SkillEntriesReturn = list[tuple[SkillIdEntry, SkillDataBase, list[ET]]]


def export_transform_skill_entries(
        transform_fn: TransformFunction, unit_data: UnitEntry, asset_manager: AssetManager,
        skip_unparsable: bool = True,
) -> tuple[SkillEntriesReturn, list[str]]:
    """Get a list of skill entries to be parsed to exported data entries."""
    ret: SkillEntriesReturn = []
    skipped_messages: list[str] = []

    is_dragon = isinstance(unit_data, DragonDataEntry)

    # Get all skills and iterate them
    skill_identifiers = unit_data.get_skill_id_entries(asset_manager, is_dragon=is_dragon)
    for id_entry in skill_identifiers:
        chara_name = unit_data.get_name(asset_manager.asset_text_multi)

        # Transform every skill data
        try:
            skill_data = transform_fn(
                id_entry.skill_id,
                unit_data.max_skill_level(id_entry.skill_num),
                unit_data.ability_ids_all_level,
            )
        except HitDataUnavailableError:
            # No attacking data available, skipping that / the skill is not an attacking skill
            continue
        except (MotionDataNotFoundError, ActionDataNotFoundError) as ex:
            # Motion file not found / Action file not found (MotionDataNotFoundError, ActionDataNotFoundError)

            if skip_unparsable:
                skipped_messages.append(f"[Skill] {id_entry.skill_identifier_labels} ({id_entry.skill_id}) "
                                        f"of {chara_name} ({unit_data.id}): {ex}")
                continue

            raise ex

        # Add skill entries and its related information
        ret.append((id_entry, skill_data, skill_data.get_all_possible_entries()))

    return ret, skipped_messages


def export_each_chara_entries(
        entry_parse_fn: CharaEntryParsingFunction, asset_manager: AssetManager, /,
        skip_unparsable: bool = True,
) -> dict[int, list[JT]]:
    """
    Parse each character to json-exportable entries.

    The key of the return is the character ID.
    To merge all entries into a single list, use ``export_entries_merged()`` instead.
    """
    ret: dict[int, list[JT]] = {}

    skipped_messages: list[str] = []

    for chara_data in asset_manager.asset_chara_data.playable_data:
        entries, messages = entry_parse_fn(chara_data, asset_manager, skip_unparsable)

        ret[chara_data.id] = entries
        skipped_messages.extend(messages)

    print_skipped_messages(skipped_messages)

    return ret


def export_each_dragon_entries(
        entry_parse_fn: DragonEntryParsingFunction, asset_manager: AssetManager, /,
        skip_unparsable: bool = True
) -> dict[int, list[JT]]:
    """
    Parse each dragon to json-exportable entries.

    The key of the return is the dragon ID.
    """
    ret: dict[int, list[JT]] = {}

    skipped_messages: list[str] = []

    for dragon_data in asset_manager.asset_dragon_data.playable_data:
        entries, messages = entry_parse_fn(dragon_data, asset_manager, skip_unparsable)

        ret[dragon_data.id] = entries
        skipped_messages.extend(messages)

    print_skipped_messages(skipped_messages)

    return ret


def export_entries_merged(
        unit_entry_parse_fn: UnitEntryParsingFunction,
        asset_manager: AssetManager, /,
        skip_unparsable: bool = True, include_dragon: bool = True
) -> list[JT]:
    """
    Parse each character and dragon to json-exportable entries.

    ``include_dragon`` indicates if the dragon data should be included to parse.

    This merges all entries from different character and dragon into a single list.
    To keep the separation, use ``export_each_chara_entries()`` or ``export_each_dragon_entries()`` instead.
    """
    ret: list[JT] = []

    chara_entry_dict = export_each_chara_entries(
        unit_entry_parse_fn, asset_manager,
        skip_unparsable=skip_unparsable,
    )
    for entries in chara_entry_dict.values():
        ret.extend(entries)

    if include_dragon:
        dragon_entry_dict = export_each_dragon_entries(
            unit_entry_parse_fn, asset_manager,
            skip_unparsable=skip_unparsable
        )
        for entries in dragon_entry_dict.values():
            ret.extend(entries)

    return ret


def export_as_csv(entries: list[CT], csv_header: list[str], file_path: str):
    """Export all ``entries`` as a csv file to ``file_path``."""
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

        writer.writerows([entry.to_csv_entry() for entry in entries])


class JsonEntryEncoder(JSONEncoder):
    """Encoder class for entries inherited from :class:`JsonExportableEntryBase`."""

    def default(self, o: Any) -> Any:
        if isinstance(o, JsonExportableEntryBase):
            return o.to_json_entry()

        return super().default(o)


def export_as_json(obj: Union[dict, list], file_path: str):
    """
    Export ``obj`` as json to ``file_path``.

    Every json export should use this function to export the data.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if needed

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        dump(obj, f, cls=JsonEntryEncoder, ensure_ascii=False, sort_keys=True)


def export_to_dir(entry_dict: dict[Union[int, str], Union[JT, list[JT]]], file_dir: str):
    """
    Export all entries in ``entry_dict`` to ``file_dir``.

    Files will be named as same as the keys of ``entry_dict``.
    Values of the corresponding key will be the file content.
    """
    for unit_id, info_entries in entry_dict.items():
        export_as_json(info_entries, os.path.join(file_dir, f"{unit_id}.json"))


def print_skipped_messages(skipped_messages: list[str]):
    """
    Placeholder method to keep track of where may have skipped messages to print.

    This can potentially indicate that some methods could be merged.
    """
    if skipped_messages:
        print()
        print(f"Some ({len(skipped_messages)}) items were skipped:")

        for msg in sorted(skipped_messages):
            print(msg)
