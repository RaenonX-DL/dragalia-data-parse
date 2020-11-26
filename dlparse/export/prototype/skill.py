"""Functions to export the skill data."""
import csv

from dlparse.errors import ActionDataNotFoundError
from dlparse.export.entry import CharaAttackingSkillEntry
from dlparse.mono.asset import CharaDataAsset, CharaDataEntry, CharaModeAsset, TextAsset
from dlparse.transformer import SkillTransformer

__all__ = ("export_skill_atk_csv",)


def export_skill_atk_csv(file_path: str, /,
                         chara_asset: CharaDataAsset, chara_mode_asset: CharaModeAsset, text_asset: TextAsset,
                         skill_transformer: SkillTransformer,
                         skip_unparsable: bool = True):
    """Export the entries of the attacking skills as csv."""
    # pylint: disable=too-many-locals

    chara_count = len(chara_asset)
    skipped_messages: list[str] = []

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CharaAttackingSkillEntry.csv_header())

        for idx, chara_data in enumerate(chara_asset):
            chara_data: CharaDataEntry

            chara_name = chara_data.get_chara_name(text_asset)
            print(f"Exporting skill data... ({idx} / {chara_count} - {idx / chara_count:.2%})")

            skill_identifiers = chara_data.get_skill_identifiers(chara_mode_asset, text_asset=text_asset)
            for skill_id, identifier, unique_id in skill_identifiers:
                try:
                    skill_data = skill_transformer.transform_attacking(skill_id)
                except (ValueError, ActionDataNotFoundError) as ex:
                    # May be unknown enum (ValueError) or action file not found (FileNotFoundError)

                    if skip_unparsable:
                        skipped_messages.append(f"[Skill] {identifier} ({skill_id}) "
                                                f"of {chara_name} ({chara_data.id}): {ex}")
                        continue

                    raise ex

                skill_name = text_asset.to_text(skill_data.skill_data_raw.name_label)

                for skill_entry in skill_data.get_all_possible_entries():
                    try:
                        entry = CharaAttackingSkillEntry(
                            character_name=chara_name,
                            character_internal_id=chara_data.id,
                            character_custom_id=chara_data.custom_id,
                            character_element=chara_data.element,
                            skill_internal_id=skill_id,
                            skill_identifier=identifier,
                            skill_unique_id=unique_id,
                            skill_name=skill_name,
                            skill_condition_comp=skill_entry.condition_comp,
                            skill_total_mods_max=skill_entry.total_mod_at_max,
                            skill_total_hits_max=skill_entry.hit_count_at_max,
                            skill_max_lv=skill_entry.max_level,
                        )
                    except IndexError as ex:
                        # REMOVE: after Eugene S1 is handled properly

                        if skip_unparsable:
                            skipped_messages.append(f"[Entry] {identifier} ({skill_id}) "
                                                    f"of {chara_name} ({chara_data.id}): {ex}")
                            continue

                        raise ex

                    writer.writerow(entry.to_csv_entry())

    if skipped_messages:
        print()
        print(f"Some ({len(skipped_messages)}) items were skipped:")

        for msg in skipped_messages:
            print(msg)
