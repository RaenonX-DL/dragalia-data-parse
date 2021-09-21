"""Classes for loading all the assets and loaders."""
import os
from typing import Optional

from dlparse.errors import ConfigError
from dlparse.transformer import (
    AbilityTransformer, AttackingActionTransformer,
    EnemyTransformer, InfoTransformer, QuestTransformer, SkillTransformer,
)
from .asset import (
    AbilityAsset, AbilityLimitGroupAsset, ActionConditionAsset, ActionGrantAsset, ActionPartsListAsset, BuffCountAsset,
    CastleStoryAsset, CharaDataAsset, CharaModeAsset, CharaUniqueComboAsset, DragonDataAsset, DungeonPlannerAsset,
    EnemyDataAsset, EnemyParamAsset, ExAbilityAsset, HitAttrAsset, MotionSelectorWeapon, PlayerActionInfoAsset,
    QuestDataAsset, QuestStoryAsset, SkillChainAsset, SkillDataAsset, TextAsset, TextAssetMultilingual, UnitStoryAsset,
    WeaponTypeAsset,
)
from .custom import WebsiteTextAsset
from .loader import ActionFileLoader, CharacterMotionLoader, DragonMotionLoader, StoryLoader

__all__ = ("AssetManager",)


class AssetManager:
    """A class for loading and managing all the assets and loaders."""

    # pylint: disable=too-many-public-methods
    # Public methods are actually properties.

    def __init__(
            self, root_resources_dir: str, /,
            is_network_source: bool = False, custom_asset_dir: Optional[str] = None
    ):
        # No need to categorize initializations. It's fine to leave all of them here
        # pylint: disable=too-many-statements

        # Paths
        if is_network_source:
            action_asset_dir = f"{root_resources_dir}/actions"
            master_asset_dir = f"{root_resources_dir}/master"
            chara_motion_asset_dir = f"{root_resources_dir}/characters/motion"
            dragon_motion_asset_dir = f"{root_resources_dir}/dragon/motion"
            story_asset_dir = f"{root_resources_dir}/story"
        else:
            action_asset_dir = os.path.join(root_resources_dir, "actions")
            master_asset_dir = os.path.join(root_resources_dir, "master")
            chara_motion_asset_dir = os.path.join(root_resources_dir, "characters", "motion")
            dragon_motion_asset_dir = os.path.join(root_resources_dir, "dragon", "motion")
            story_asset_dir = os.path.join(root_resources_dir, "story")

        # Master Assets
        # --- Battle-related (Player)
        self._asset_ability_data = AbilityAsset(asset_dir=master_asset_dir)
        self._asset_ability_limit = AbilityLimitGroupAsset(asset_dir=master_asset_dir)
        self._asset_action_cond = ActionConditionAsset(asset_dir=master_asset_dir)
        self._asset_action_grant = ActionGrantAsset(asset_dir=master_asset_dir)
        self._asset_buff_count = BuffCountAsset(asset_dir=master_asset_dir)
        self._asset_chara_data = CharaDataAsset(asset_dir=master_asset_dir)
        self._asset_chara_mode = CharaModeAsset(asset_dir=master_asset_dir)
        self._asset_chara_unique_combo = CharaUniqueComboAsset(asset_dir=master_asset_dir)
        self._asset_dragon_data = DragonDataAsset(asset_dir=master_asset_dir)
        self._asset_ex_ability = ExAbilityAsset(asset_dir=master_asset_dir)
        self._asset_hit_attr = HitAttrAsset(asset_dir=master_asset_dir)
        self._asset_skill_data = SkillDataAsset(asset_dir=master_asset_dir)
        self._asset_skill_chain = SkillChainAsset(asset_dir=master_asset_dir)

        # --- Battle-related (Enemy)
        self._asset_dungeon_planner = DungeonPlannerAsset(asset_dir=master_asset_dir)
        self._asset_enemy_data = EnemyDataAsset(asset_dir=master_asset_dir)
        self._asset_enemy_param = EnemyParamAsset(asset_dir=master_asset_dir)
        self._asset_quest_data = QuestDataAsset(asset_dir=master_asset_dir)

        # --- Actions
        self._asset_pa_info = PlayerActionInfoAsset(asset_dir=master_asset_dir)
        self._asset_action_list = ActionPartsListAsset(asset_dir=action_asset_dir)

        # --- Story
        self._asset_story_main = QuestStoryAsset(asset_dir=master_asset_dir)
        self._asset_story_unit = UnitStoryAsset(asset_dir=master_asset_dir)
        self._asset_story_castle = CastleStoryAsset(asset_dir=master_asset_dir)

        # --- Misc
        self._asset_text = TextAsset(asset_dir=master_asset_dir, custom_asset_dir=custom_asset_dir)

        self._asset_text_multi = TextAssetMultilingual(master_asset_dir)
        self._asset_weapon_type = WeaponTypeAsset(asset_dir=master_asset_dir)

        # Motion Assets
        self._motion_weapon = MotionSelectorWeapon(chara_motion_asset_dir)

        # Custom Assets
        # - If custom asset directory is not provided, do not load the asset
        self._asset_text_website = WebsiteTextAsset(asset_dir=custom_asset_dir) if custom_asset_dir else None

        # Loaders
        self._loader_action = ActionFileLoader(self._asset_action_list, action_asset_dir)
        self._loader_chara_motion = CharacterMotionLoader(chara_motion_asset_dir)
        self._loader_dragon_motion = DragonMotionLoader(dragon_motion_asset_dir)
        self._loader_story = StoryLoader(story_asset_dir, self)

        # Transformers
        self._transformer_ability = AbilityTransformer(self)
        self._transformer_atk = AttackingActionTransformer(self)
        self._transformer_enemy = EnemyTransformer(self)
        self._transformer_info = InfoTransformer(self)
        self._transformer_skill = SkillTransformer(self)
        self._transformer_quest = QuestTransformer(self)

    # region Master Assets

    # --- Battle-related (Player)

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
    def asset_chara_unique_combo(self) -> CharaUniqueComboAsset:
        """Get the character unique combo asset."""
        return self._asset_chara_unique_combo

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
    def asset_text_multi(self) -> TextAssetMultilingual:
        """Get the multilingual text label asset."""
        return self._asset_text_multi

    @property
    def asset_weapon_type(self) -> WeaponTypeAsset:
        """Get the weapon type asset."""
        return self._asset_weapon_type

    # --- Battle-related (Enemy)

    @property
    def asset_dungeon_planner(self) -> DungeonPlannerAsset:
        """Get the dungeon planner asset."""
        return self._asset_dungeon_planner

    @property
    def asset_enemy_data(self) -> EnemyDataAsset:
        """Get the enemy data."""
        return self._asset_enemy_data

    @property
    def asset_enemy_param(self) -> EnemyParamAsset:
        """Get the enemy param data."""
        return self._asset_enemy_param

    @property
    def asset_quest_data(self) -> QuestDataAsset:
        """Get the quest data asset."""
        return self._asset_quest_data

    # --- Actions

    @property
    def asset_action_info_player(self) -> PlayerActionInfoAsset:
        """Get the player action info asset."""
        return self._asset_pa_info

    @property
    def asset_action_list(self) -> ActionPartsListAsset:
        """Get the action parts list asset."""
        return self._asset_action_list

    # --- Story

    @property
    def asset_story_main(self) -> QuestStoryAsset:
        """Get the main quest story asset."""
        return self._asset_story_main

    @property
    def asset_story_unit(self) -> UnitStoryAsset:
        """Get the unit story asset."""
        return self._asset_story_unit

    @property
    def asset_story_castle(self) -> CastleStoryAsset:
        """Get the castle story asset."""
        return self._asset_story_castle

    # --- Misc

    @property
    def asset_text(self) -> TextAsset:
        """Get the text label asset."""
        return self._asset_text

    # endregion

    # region Motion Assets
    @property
    def motion_weapon(self) -> MotionSelectorWeapon:
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
            raise ConfigError("Custom asset directory not specified. "
                              "Specify the custom asset directory then try again.")

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

    @property
    def loader_story(self) -> StoryLoader:
        """Get the story data loader."""
        return self._loader_story

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

    @property
    def transformer_atk(self) -> AttackingActionTransformer:
        """Get the attacking action transformer."""
        return self._transformer_atk

    @property
    def transformer_enemy(self) -> EnemyTransformer:
        """Get the enemy data transformer."""
        return self._transformer_enemy

    @property
    def transformer_info(self) -> InfoTransformer:
        """Get the info transformer."""
        return self._transformer_info

    @property
    def transformer_quest(self) -> QuestTransformer:
        """Get the quest data transformer."""
        return self._transformer_quest

    # endregion

    # endregion

    @property
    def chara_count(self) -> int:
        """Get the count of the available characters, including the unplayable ones."""
        return len(self.asset_chara_data)
