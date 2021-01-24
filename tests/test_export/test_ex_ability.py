from dlparse.export import export_ex_abilities_as_entries
from dlparse.mono.manager import AssetManager


def test_exported_json(asset_manager: AssetManager):
    entries = export_ex_abilities_as_entries(asset_manager)

    for entry in entries:
        json_entry = entry.to_json_entry()

        # Check for first level keys
        for first_level_key in ("chara", "ex", "chainedEx"):
            assert first_level_key in json_entry

        # Check for character keys
        for chara_key in ("iconName", "name", "element"):
            assert chara_key in json_entry["chara"]

        effect_unit_keys = {
            # Effect unit base
            "status", "target", "parameter", "paramUnit", "probabilityPct", "rate", "slipInterval", "slipDamageMod",
            "durationSec", "durationCount", "maxStackCount", "stackable",
            # Ability variants
            "sourceAbilityId", "conditions", "cooldownSec", "maxOccurrences", "rateMax", "targetAction"
        }

        # Check for effect unit keys (EX)
        for ex_unit in json_entry["ex"]:
            # Check sub-keys in parameter
            assert set(ex_unit["parameter"]) == {"name", "code", "imagePath"}
            assert set(ex_unit["paramUnit"]) == {"name", "code", "isPercentage"}

            expected_keys = effect_unit_keys
            actual_keys = set(ex_unit)

            diff = expected_keys.symmetric_difference(actual_keys)

            assert not diff, diff

        # Check for effect unit keys (CEX)
        for ex_unit in json_entry["chainedEx"]:
            # Check sub-keys in parameter
            assert set(ex_unit["parameter"]) == {"name", "code", "imagePath"}
            assert set(ex_unit["paramUnit"]) == {"name", "code", "isPercentage"}

            expected_keys = effect_unit_keys
            actual_keys = set(ex_unit)

            diff = expected_keys.symmetric_difference(actual_keys)

            assert not diff, diff
