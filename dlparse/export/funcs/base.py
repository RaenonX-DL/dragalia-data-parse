"""Base exporting functions."""
import csv
import json
import os
from json import JSONEncoder
from typing import Any, Callable, TypeVar, Union

from dlparse.errors import ActionDataNotFoundError, HitDataUnavailableError, MotionDataNotFoundError
from dlparse.export.entry import CsvExportableEntryBase, JsonExportableEntryBase, SkillExportEntryBase
from dlparse.model import SkillDataBase
from dlparse.mono.asset import CharaDataEntry, SkillIdEntry
from dlparse.mono.manager import AssetManager

__all__ = ("export_as_csv", "export_as_json", "export_skill_entries", "export_transform_skill_entries")

CT = TypeVar("CT", bound=CsvExportableEntryBase)
ET = TypeVar("ET", bound=SkillExportEntryBase)
DT = TypeVar("DT", bound=SkillDataBase)

SkillEntryParsingFunction = Callable[
    [CharaDataEntry, AssetManager, bool, bool],
    tuple[list[ET], list[str]]
]

TransformFunction = Callable[
    [int, int],
    DT
]

SkillEntriesReturn = list[tuple[SkillIdEntry, SkillDataBase, list[ET]]]


def export_transform_skill_entries(
        transform_fn: TransformFunction, chara_data: CharaDataEntry, asset_manager: AssetManager,
        skip_unparsable: bool = True, include_dragon: bool = True
) -> tuple[SkillEntriesReturn, list[str]]:
    """Get a list of skill entries to be parsed to exported data entries."""
    ret: SkillEntriesReturn = []
    skipped_messages: list[str] = []

    # Get all skills and iterate them
    skill_identifiers = chara_data.get_skill_id_entries(asset_manager, include_dragon=include_dragon)
    for id_entry in skill_identifiers:
        chara_name = chara_data.get_chara_name(asset_manager.asset_text)

        # Transform every skill data
        try:
            skill_data = transform_fn(
                id_entry.skill_id,
                chara_data.max_skill_level(id_entry.skill_num)
            )
        except HitDataUnavailableError:
            # No attacking data available, skipping that / the skill is not an attacking skill
            continue
        except (MotionDataNotFoundError, ActionDataNotFoundError) as ex:
            # Motion file not found / Action file not found (MotionDataNotFoundError, ActionDataNotFoundError)

            if skip_unparsable:
                skipped_messages.append(f"[Skill] {id_entry.skill_identifier_labels} ({id_entry.skill_id}) "
                                        f"of {chara_name} ({chara_data.id}): {ex}")
                continue

            raise ex

        # Add skill entries and its related information
        ret.append((id_entry, skill_data, skill_data.get_all_possible_entries()))

    return ret, skipped_messages


def export_skill_entries(
        skill_entry_parse_fn: SkillEntryParsingFunction, asset_manager: AssetManager, /,
        skip_unparsable: bool = True, include_dragon: bool = True
) -> list[ET]:
    """Export skill entries of all characters to a list of data entries ready to be exported."""
    ret: list[ET] = []

    skipped_messages: list[str] = []

    for chara_data in asset_manager.asset_chara_data.playable_chara_data:
        entries, messages = skill_entry_parse_fn(chara_data, asset_manager, skip_unparsable, include_dragon)

        ret.extend(entries)
        skipped_messages.extend(messages)

    if skipped_messages:
        print()
        print(f"Some ({len(skipped_messages)}) items were skipped:")

        for msg in skipped_messages:
            print(msg)

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
        json.dump(obj, f, cls=JsonEntryEncoder, ensure_ascii=False, sort_keys=True)
