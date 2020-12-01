from dlparse.export.prototype import export_skill_atk_csv
from dlparse.mono.asset import (
    CharaDataAsset, CharaModeAsset, TextAsset, SkillDataAsset, HitAttrAsset, ActionConditionAsset,
    AbilityAsset
)
from dlparse.mono.loader import PlayerActionFileLoader
from dlparse.transformer import SkillTransformer
from tests.static import PATH_DIR_MASTER_ASSET, PATH_ROOT_ASSET_PLAYER_ACTION

# Asset instances
_chara_data: CharaDataAsset = CharaDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_text: TextAsset = TextAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_action_cond: ActionConditionAsset = ActionConditionAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_ability_asset: AbilityAsset = AbilityAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_pa_loader: PlayerActionFileLoader = PlayerActionFileLoader(PATH_ROOT_ASSET_PLAYER_ACTION)

# Transformers
_transformer_skill: SkillTransformer = SkillTransformer(_skill_data, _hit_attr, _action_cond, _pa_loader,
                                                        _ability_asset)


def main():
    export_skill_atk_csv(
        "exported/skill_atk.csv",
        chara_asset=_chara_data, chara_mode_asset=_chara_mode, text_asset=_text, skill_transformer=_transformer_skill
    )


def main2():
    skill_id = 101504043
    skill_name = "Peco S1-2"

    skill_data = _transformer_skill.transform_attacking(skill_id)

    print(f"{skill_name} ({skill_id})")
    print("=" * 30)
    for skill_entry in skill_data.get_all_possible_entries():
        print(f"Conditions: {skill_entry.condition_comp.conditions_sorted}")
        print()

        for skill_level in range(skill_entry.max_level):
            print(f"Lv.{skill_level + 1} {'(max)' if skill_entry.max_level == skill_level else ''}")
            print()
            print(f"Mods distribution: {skill_entry.mods[skill_level]}")
            print(f"Total Mods: {skill_entry.total_mod[skill_level]:.0%} ({skill_entry.hit_count[skill_level]} hits)")
            print()


if __name__ == '__main__':
    main2()
