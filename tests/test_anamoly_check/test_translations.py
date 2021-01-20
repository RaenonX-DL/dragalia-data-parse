from dlparse.enums import Condition, Language
from dlparse.mono.manager import AssetManager


def test_condition_enum_translations(asset_manager: AssetManager):
    names_enum = {f"ENUM_COND_{condition.name}" for condition in Condition}

    for lang_code in Language.get_all_available_codes():
        names_translations = {
            name for name in asset_manager.asset_text_website.get_all_ids(lang_code) if name.startswith("ENUM_COND")
        }

        assert \
            names_enum == names_translations, \
            f"Difference in `{lang_code}`:\n" \
            f"# Additional in condition enum:\n" \
            f"{names_enum.difference(names_translations)}\n" \
            f"# Additional in translation:\n" \
            f"{names_translations.difference(names_enum)}"
