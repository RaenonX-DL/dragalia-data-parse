from dlparse.export import export_atk_skill_as_csv, export_sup_skill_as_csv
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


def export_atk():
    export_atk_skill_as_csv(
        "exported/skill_atk.csv",
        chara_asset=_chara_data, chara_mode_asset=_chara_mode, text_asset=_text, skill_transformer=_transformer_skill
    )


def export_sup():
    export_sup_skill_as_csv(
        "exported/skill_sup.csv",
        chara_asset=_chara_data, chara_mode_asset=_chara_mode, text_asset=_text, skill_transformer=_transformer_skill
    )


if __name__ == '__main__':
    export_sup()
