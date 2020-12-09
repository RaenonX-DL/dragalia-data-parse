"""Classes for loading all the assets and loaders."""
from typing import Optional

from dlparse.transformer import SkillTransformer
from .asset import (
    AbilityAsset, ActionConditionAsset, CharaDataAsset, CharaModeAsset, DragonDataAsset, HitAttrAsset,
    PlayerActionInfoAsset, SkillChainAsset, SkillDataAsset, TextAsset,
)
from .loader import PlayerActionFileLoader

__all__ = ("AssetManager",)


class AssetManager:
    """A class for loading and managing all the assets and loaders."""

    def __init__(self, player_action_dir: str, master_asset_dir: str, custom_asset_dir: Optional[str] = None):
        # Assets
        self._asset_ability_data: AbilityAsset = AbilityAsset(asset_dir=master_asset_dir)
        self._asset_action_cond: ActionConditionAsset = ActionConditionAsset(asset_dir=master_asset_dir)
        self._asset_chara_data: CharaDataAsset = CharaDataAsset(asset_dir=master_asset_dir)
        self._asset_chara_mode: CharaModeAsset = CharaModeAsset(asset_dir=master_asset_dir)
        self._asset_dragon: DragonDataAsset = DragonDataAsset(asset_dir=master_asset_dir)
        self._asset_hit_attr: HitAttrAsset = HitAttrAsset(asset_dir=master_asset_dir)
        self._asset_skill: SkillDataAsset = SkillDataAsset(asset_dir=master_asset_dir)
        self._asset_skill_chain: SkillChainAsset = SkillChainAsset(asset_dir=master_asset_dir)
        self._asset_text: TextAsset = TextAsset(asset_dir=master_asset_dir, asset_dir_custom=custom_asset_dir)
        self._asset_pa_info: PlayerActionInfoAsset = PlayerActionInfoAsset(asset_dir=master_asset_dir)

        # Loaders
        self._loader_pa: PlayerActionFileLoader = PlayerActionFileLoader(player_action_dir)

        # Transformers
        self._transformer_skill: SkillTransformer = SkillTransformer(self)

    # region Assets / Loaders / Transformers
    @property
    def asset_ability_data(self) -> AbilityAsset:
        """Get the ability data asset."""
        return self._asset_ability_data

    @property
    def asset_action_cond(self) -> ActionConditionAsset:
        """Get the action condition data asset."""
        return self._asset_action_cond

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
    def asset_skill(self) -> SkillDataAsset:
        """Get the skill data asset."""
        return self._asset_skill

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
    def loader_pa(self) -> PlayerActionFileLoader:
        """Get the player action file loader."""
        return self._loader_pa

    @property
    def transformer_skill(self) -> SkillTransformer:
        """Get the skill transformer."""
        return self._transformer_skill

    # endregion

    @property
    def chara_count(self) -> int:
        """Get the count of the available characters, including the unplayable ones."""
        return len(self.asset_chara_data)
