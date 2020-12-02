"""Functions to export the skill data."""
import csv

from dlparse.errors import ActionDataNotFoundError, HitDataUnavailableError
from dlparse.export.entry import CharaAttackingSkillEntry
from dlparse.mono.asset import CharaDataAsset, CharaDataEntry, CharaModeAsset, TextAsset
from dlparse.transformer import SkillTransformer

__all__ = ("export_atk_skill_as_csv", "export_atk_skills_as_entries")


def export_atk_skills_of_chara(chara_data: CharaDataEntry, chara_mode_asset: CharaModeAsset, text_asset: TextAsset,
                               skill_transformer: SkillTransformer,
                               skip_unparsable: bool = True) -> tuple[list[CharaAttackingSkillEntry], list[str]]:
    """Export attacking skills of a character as entries."""
    ret: list[CharaAttackingSkillEntry] = []
    skipped_messages: list[str] = []

    # Get all skills and iterate them
    skill_identifiers = chara_data.get_skill_identifiers(chara_mode_asset, asset_text=text_asset)
    for id_entry in skill_identifiers:
        chara_name = chara_data.get_chara_name(text_asset)

        # Transform every skill data
        try:
            skill_data = skill_transformer.transform_attacking(
                id_entry.skill_id,
                max_lv=chara_data.max_skill_level(id_entry.skill_num)
            )
        except HitDataUnavailableError:
            # No attacking data available, skipping that
            continue
        except (ValueError, ActionDataNotFoundError) as ex:
            # May be unknown enum (ValueError) or action file not found (FileNotFoundError)

            if skip_unparsable:
                skipped_messages.append(f"[Skill] {id_entry.skill_identifier} ({id_entry.skill_id}) "
                                        f"of {chara_name} ({chara_data.id}): {ex}")
                continue

            raise ex

        skill_name = text_asset.to_text(skill_data.skill_data_raw.name_label)

        # Transform every skill entries
        for skill_entry in skill_data.get_all_possible_entries():
            try:
                ret.append(CharaAttackingSkillEntry(
                    character_name=chara_name,
                    character_internal_id=chara_data.id,
                    character_custom_id=chara_data.custom_id,
                    character_element=chara_data.element,
                    skill_internal_id=id_entry.skill_id,
                    skill_identifier=id_entry.skill_identifier,
                    skill_name=skill_name,
                    skill_condition_comp=skill_entry.condition_comp,
                    skill_total_mods_max=skill_entry.total_mod_at_max,
                    skill_total_hits_max=skill_entry.hit_count_at_max,
                    skill_max_lv=skill_entry.max_level,
                ))
            except IndexError as ex:
                # REMOVE: all skills can be handled properly (Eugene S1)

                if skip_unparsable:
                    skipped_messages.append(f"[Entry] {id_entry.skill_identifier} ({id_entry.skill_id}) "
                                            f"of {chara_name} ({chara_data.id}): {ex}")
                    continue

                raise ex

    return ret, skipped_messages


def export_atk_skills_as_entries(chara_asset: CharaDataAsset, chara_mode_asset: CharaModeAsset, text_asset: TextAsset,
                                 skill_transformer: SkillTransformer,
                                 skip_unparsable: bool = True) -> list[CharaAttackingSkillEntry]:
    """Export attacking skills of all characters to be a list of data entries ready to be exported."""
    # pylint: disable=too-many-locals

    ret: list[CharaAttackingSkillEntry] = []

    chara_count = len(chara_asset)
    skipped_messages: list[str] = []

    for idx, chara_data in enumerate(chara_asset):
        chara_data: CharaDataEntry
        if not chara_data.is_playable:
            print(f"Character ID: {chara_data.id} not playable, skipping.")
            continue

        print(f"Exporting skill data... ({idx} / {chara_count} - {idx / chara_count:.2%})")

        entries, messages = export_atk_skills_of_chara(chara_data, chara_mode_asset, text_asset,
                                                       skill_transformer, skip_unparsable)

        ret.extend(entries)
        skipped_messages.extend(messages)

    if skipped_messages:
        print()
        print(f"Some ({len(skipped_messages)}) items were skipped:")

        for msg in skipped_messages:
            print(msg)

    return ret


def export_atk_skill_as_csv(file_path: str, /,  # noqa: C901
                            chara_asset: CharaDataAsset, chara_mode_asset: CharaModeAsset, text_asset: TextAsset,
                            skill_transformer: SkillTransformer,
                            skip_unparsable: bool = True):
    """Export the entries of the attacking skills as csv."""
    entries = export_atk_skills_as_entries(chara_asset, chara_mode_asset, text_asset,
                                           skill_transformer, skip_unparsable)

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CharaAttackingSkillEntry.csv_header())

        writer.writerows([entry.to_csv_entry() for entry in entries])
