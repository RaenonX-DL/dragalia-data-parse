from dlparse.export.prototype import export_skill_atk_csv
from dlparse.mono.asset import CharaDataAsset, CharaModeAsset, TextAsset, SkillDataAsset, HitAttrAsset
from dlparse.mono.loader import PlayerActionFileLoader
from dlparse.transformer import SkillTransformer
from tests.static import PATH_DIR_MASTER_ASSET, PATH_ROOT_ASSET_PLAYER_ACTION

# Asset instances
_chara_data: CharaDataAsset = CharaDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_text: TextAsset = TextAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=PATH_DIR_MASTER_ASSET)
_pa_path_finder: PlayerActionFileLoader = PlayerActionFileLoader(PATH_ROOT_ASSET_PLAYER_ACTION)

# Transformets
_transformer_skill: SkillTransformer = SkillTransformer(_skill_data, _hit_attr, _pa_path_finder)


def main():
    export_skill_atk_csv(
        "exported/skill_atk.csv",
        chara_asset=_chara_data, chara_mode_asset=_chara_mode, text_asset=_text, skill_transformer=_transformer_skill
    )


if __name__ == '__main__':
    main()
