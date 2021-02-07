"""Classes for loading all the assets and loaders."""
from typing import Optional

from dlparse.enums import Language
from dlparse.errors import ConfigError
from dlparse.transformer import AbilityTransformer, SkillTransformer
from .asset import (
    AbilityAsset, AbilityLimitGroupAsset, ActionConditionAsset, ActionGrantAsset, ActionPartsListAsset, BuffCountAsset,
    CharaDataAsset, CharaModeAsset, DragonDataAsset, ExAbilityAsset, HitAttrAsset, MotionSelectorWeapon,
    PlayerActionInfoAsset, SkillChainAsset, SkillDataAsset, TextAsset, TextAssetMultilingual,
)
from .custom import WebsiteTextAsset
from .loader import ActionFileLoader, CharacterMotionLoader, DragonMotionLoader

__all__ = ("AssetManager",)


class AssetManager:
    """A class for loading and managing all the assets and loaders."""

    # pylint: disable=too-many-public-methods
    # Public methods are actually properties.

    def __init__(
            self, action_asset_dir: str, master_asset_dir: str, chara_motion_asset_dir: str,
            dragon_motion_asset_dir: str, /,
            custom_asset_dir: Optional[str] = None
    ):
        # Master Assets
        self._asset_ability_data = AbilityAsset(asset_dir=master_asset_dir)
        self._asset_ability_limit = AbilityLimitGroupAsset(asset_dir=master_asset_dir)
        self._asset_action_cond = ActionConditionAsset(asset_dir=master_asset_dir)
        self._asset_action_grant = ActionGrantAsset(asset_dir=master_asset_dir)
        self._asset_buff_count = BuffCountAsset(asset_dir=master_asset_dir)
        self._asset_chara_data = CharaDataAsset(asset_dir=master_asset_dir)
        self._asset_chara_mode = CharaModeAsset(asset_dir=master_asset_dir)
        self._asset_dragon_data = DragonDataAsset(asset_dir=master_asset_dir)
        self._asset_ex_ability = ExAbilityAsset(asset_dir=master_asset_dir)
        self._asset_hit_attr = HitAttrAsset(asset_dir=master_asset_dir)
        self._asset_skill_data = SkillDataAsset(asset_dir=master_asset_dir)
        self._asset_skill_chain = SkillChainAsset(asset_dir=master_asset_dir)
        self._asset_text = TextAsset(asset_dir=master_asset_dir, custom_asset_dir=custom_asset_dir)
        self._asset_pa_info = PlayerActionInfoAsset(asset_dir=master_asset_dir)
        self._asset_action_list = ActionPartsListAsset(asset_dir=action_asset_dir)

        lang_code_mapping = {
            "en": Language.EN.value,
            "tw": Language.CHT.value,
            "": Language.JP.value
        }
        self._asset_text_multi = TextAssetMultilingual(lang_code_mapping, master_asset_dir)

        # Motion Assets
        self._motion_weapon = MotionSelectorWeapon(chara_motion_asset_dir)

        # Custom Assets
        self._asset_text_website: WebsiteTextAsset = WebsiteTextAsset(
            Language.get_all_available_codes(),
            asset_dir=custom_asset_dir
        ) if custom_asset_dir else None  # If custom asset directory is not provided, do not load the asset

        # Loaders
        self._loader_action = ActionFileLoader(self._asset_action_list, action_asset_dir)
        self._loader_chara_motion = CharacterMotionLoader(chara_motion_asset_dir)
        self._loader_dragon_motion = DragonMotionLoader(dragon_motion_asset_dir)

        # Transformers
        self._transformer_ability = AbilityTransformer(self)
        self._transformer_skill = SkillTransformer(self)

    # region Master Assets
    @property
    def asset_ability_data(self) -> AbilityAsset:
        """Get the ability data asset."""
        return self._asset_ability_data

    @property
    def asset_ability_limit(self) -> AbilityLimitGroupAsset:
        """Get the ability limit data asset."""
        return self._asset_ability_limit

    @property
    def asset_action_cond(self) -> ActionConditionAsset:
        """Get the action condition data asset."""
        return self._asset_action_cond

    @property
    def asset_action_grant(self) -> ActionGrantAsset:
        """Get the action grant asset."""
        return self._asset_action_grant

    @property
    def asset_buff_count(self) -> BuffCountAsset:
        """Get the buff count data asset."""
        return self._asset_buff_count

    @property
    def asset_chara_data(self) -> CharaDataAsset:
        """Get the character data asset."""
        return self._asset_chara_data

    @property
    def asset_chara_mode(self) -> CharaModeAsset:
        """Get the character mode asset."""
        return self._asset_chara_mode

    @property
    def asset_dragon_data(self) -> DragonDataAsset:
        """Get the dragon data asset."""
        return self._asset_dragon_data

    @property
    def asset_ex_ability(self) -> ExAbilityAsset:
        """Get the EX ability data asset."""
        return self._asset_ex_ability

    @property
    def asset_hit_attr(self) -> HitAttrAsset:
        """Get the hit attribute asset."""
        return self._asset_hit_attr

    @property
    def asset_skill_data(self) -> SkillDataAsset:
        """Get the skill data asset."""
        return self._asset_skill_data

    @property
    def asset_skill_chain(self) -> SkillChainAsset:
        """Get the skill chain data asset."""
        return self._asset_skill_chain

    @property
    def asset_text(self) -> TextAsset:
        """Get the text label asset."""
        return self._asset_text

    @property
    def asset_text_multi(self) -> TextAssetMultilingual:
        """Get the multilingual text label asset."""
        return self._asset_text_multi

    @property
    def asset_action_info_player(self) -> PlayerActionInfoAsset:
        """Get the player action info asset."""
        return self._asset_pa_info

    @property
    def asset_action_list(self) -> ActionPartsListAsset:
        """Get the action parts list asset."""
        return self._asset_action_list

    # endregion

    # region Motion Assets
    @property
    def motion_weapon(self):
        """Get the character weapon motion asset."""
        return self._motion_weapon

    # endregion

    # region Custom Assets
    @property
    def asset_text_website(self) -> WebsiteTextAsset:
        """
        Get the asset for the website texts.

        :raises ConfigError: if custom asset directory was not given
        """
        if not self._asset_text_website:
            # Case when the custom asset directory was not given
            raise ConfigError("Custom asset directory was not given. "
                              "Specify the custom asset directory then call this again.")

        return self._asset_text_website

    # endregion

    # region Loaders
    @property
    def loader_action(self) -> ActionFileLoader:
        """Get the action file loader."""
        return self._loader_action

    @property
    def loader_chara_motion(self) -> CharacterMotionLoader:
        """Get the character motion loader."""
        return self._loader_chara_motion

    @property
    def loader_dragon_motion(self) -> DragonMotionLoader:
        """Get the dragon motion loader."""
        return self._loader_dragon_motion

    # endregion

    # region Transformers
    @property
    def transformer_skill(self) -> SkillTransformer:
        """Get the skill transformer."""
        return self._transformer_skill

    @property
    def transformer_ability(self) -> AbilityTransformer:
        """Get the ability transformer."""
        return self._transformer_ability

    # endregion

    # endregion

    @property
    def chara_count(self) -> int:
        """Get the count of the available characters, including the unplayable ones."""
        return len(self.asset_chara_data)
