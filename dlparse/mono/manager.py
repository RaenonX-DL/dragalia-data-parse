"""Classes for loading all the assets and loaders."""
from typing import Optional

from dlparse.transformer import SkillTransformer
from .asset import (
    AbilityAsset, ActionConditionAsset, ActionPartsListAsset, BuffCountAsset, CharaDataAsset, CharaModeAsset,
    DragonDataAsset, HitAttrAsset, PlayerActionInfoAsset, SkillChainAsset, SkillDataAsset, TextAsset,
)
from .loader import ActionFileLoader

__all__ = ("AssetManager",)


class AssetManager:
    """A class for loading and managing all the assets and loaders."""

    def __init__(
            self, action_asset_dir: str, master_asset_dir: str, /,
            custom_asset_dir: Optional[str] = None
    ):
        # Assets
        self._asset_ability_data: AbilityAsset = AbilityAsset(asset_dir=master_asset_dir)
        self._asset_action_cond: ActionConditionAsset = ActionConditionAsset(asset_dir=master_asset_dir)
        self._asset_buff_count: BuffCountAsset = BuffCountAsset(asset_dir=master_asset_dir)
        self._asset_chara_data: CharaDataAsset = CharaDataAsset(asset_dir=master_asset_dir)
        self._asset_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=master_asset_dir)
        self._asset_dragon: DragonDataAsset = DragonDataAsset(asset_dir=master_asset_dir)
        self._asset_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=master_asset_dir)
        self._asset_skill_data: SkillDataAsset = SkillDataAsset(asset_dir=master_asset_dir)
        self._asset_skill_chain: SkillChainAsset = SkillChainAsset(asset_dir=master_asset_dir)
        self._asset_text: TextAsset = TextAsset(asset_dir=master_asset_dir, custom_asset_dir=custom_asset_dir)
        self._asset_pa_info: PlayerActionInfoAsset = PlayerActionInfoAsset(asset_dir=master_asset_dir)
        self._asset_action_list: ActionPartsListAsset = ActionPartsListAsset(asset_dir=action_asset_dir)

        # Loaders
        self._loader_action: ActionFileLoader = ActionFileLoader(self._asset_action_list, action_asset_dir)

        # Transformers
        self._transformer_skill: SkillTransformer = SkillTransformer(self)

    # region Assets
    @property
    def asset_ability_data(self) -> AbilityAsset:
        """Get the ability data asset."""
        return self._asset_ability_data

    @property
    def asset_action_cond(self) -> ActionConditionAsset:
        """Get the action condition data asset."""
        return self._asset_action_cond

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
    def asset_dragon(self) -> DragonDataAsset:
        """Get the dragon data asset."""
        return self._asset_dragon

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
    def asset_pa_info(self) -> PlayerActionInfoAsset:
        """Get the player action info asset."""
        return self._asset_pa_info

    @property
    def asset_action_list(self) -> ActionPartsListAsset:
        """Get the action parts list asset."""
        return self._asset_action_list
    # endregion

    # region Loaders
    @property
    def loader_action(self) -> ActionFileLoader:
        """Get the action file loader."""
        return self._loader_action
    # endregion

    # region Transformers
    @property
    def transformer_skill(self) -> SkillTransformer:
        """Get the skill transformer."""
        return self._transformer_skill
    # endregion

    # endregion

    @property
    def chara_count(self) -> int:
        """Get the count of the available characters, including the unplayable ones."""
        return len(self.asset_chara_data)
