"""Skill data transformer."""
from typing import Optional, Type, TypeVar

from dlparse.errors import HitDataUnavailableError, SkillDataNotFoundError
from dlparse.model import AttackingSkillData, BuffingHitData, DamagingHitData, HitData, SupportiveSkillData
from dlparse.mono.asset import (
    AbilityAsset, ActionConditionAsset, HitAttrAsset, PlayerActionInfoAsset, SkillDataAsset, SkillDataEntry,
)
from dlparse.mono.loader import PlayerActionFileLoader

__all__ = ("SkillTransformer",)

T = TypeVar("T", bound=HitData)

HitDataList = list[T]


class SkillTransformer:
    """Class to transform the skill data."""

    def __init__(self, skill_data_asset: SkillDataAsset, hit_attr_asset: HitAttrAsset,
                 action_condition_asset: ActionConditionAsset, action_loader: PlayerActionFileLoader,
                 ability_asset: AbilityAsset, action_info_asset: PlayerActionInfoAsset):
        self._skill_data = skill_data_asset
        self._hit_attr = hit_attr_asset
        self._action_cond = action_condition_asset
        self._action_loader = action_loader
        self._action_info = action_info_asset
        self._ability_asset = ability_asset

    @property
    def skill_data_asset(self) -> SkillDataAsset:
        """Get the skill data asset used by this transformer."""
        return self._skill_data

    def _get_hit_data_lv(self, hit_data_cls: Type[T], skill_lv: int, action_id: int, ability_id: int) -> HitDataList:
        """Get a list of hit attributes at a certain ``skill_lv``."""
        ret: HitDataList = []

        # --- From action component
        for hit_label, action_component in self._action_loader.get_prefab(action_id).get_hit_actions(skill_lv):
            # If the hit attribute is missing, just skip it; sometimes it's simply missing
            if hit_attr_data := self._hit_attr.get_data_by_id(hit_label):
                ret.append(hit_data_cls(hit_attr=hit_attr_data, action_component=action_component, action_id=action_id,
                                        pre_condition=action_component.condition_data.skill_pre_condition))

        # --- From ability
        if init_ability_data := self._ability_asset.get_data_by_id(ability_id):
            # Get all ability data from the condition chain
            ability_data_queue = [init_ability_data]

            while ability_data_queue:
                # Pop an ability data from the frontier
                ability_data = ability_data_queue.pop(0)

                # Parse to :class:`HitData` and attach it to the hit attribute list to be returned
                for hit_label in ability_data.assigned_hit_labels:
                    # If the hit attribute is missing, just skip it; sometimes it's simply missing
                    if hit_attr_data := self._hit_attr.get_data_by_id(hit_label):
                        ret.append(hit_data_cls(hit_attr=hit_attr_data, action_component=None, action_id=action_id,
                                                pre_condition=ability_data.condition.to_skill_condition()))

                # Add all ability data to be used upon condition mismatch to the ability data queue
                for other_ability_id in ability_data.get_other_ability_ids:
                    if new_frontier := self._ability_asset.get_data_by_id(other_ability_id):
                        ability_data_queue.append(new_frontier)

        return ret

    def get_hit_data_matrix(
            self, skill_id: int, hit_data_cls: Type[T], /,
            deals_damage: bool = True, max_lv: int = 0
    ) -> tuple[SkillDataEntry, list[list[T]]]:
        """
        Get a matrix of the hit data.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        The first index of the matrix is the skill level (Skill level 1 = index 0).

        :raises SkillDataNotFoundError: skill data not found
        :raises ActionDataNotFoundError: action file not found
        :raises HitDataUnavailableError: no hit data available
        """
        # Get the skill data
        skill_data: Optional[SkillDataEntry] = self._skill_data.get_data_by_id(skill_id)
        if not skill_data:
            raise SkillDataNotFoundError(skill_id)

        # Get hit attribute data
        hit_data_mtx: list[list[T]] = []

        # Get all hit labels at different skill level
        if max_lv:
            # Limit the count of IDs can be zipped if ``max_lv`` is given
            zipped_ids = list(zip(skill_data.action_id_1_by_level, skill_data.ability_id_by_level))[:max_lv]
        else:
            # No ``max_lv`` given, returning all possiblities
            zipped_ids = zip(skill_data.action_id_1_by_level, skill_data.ability_id_by_level)

        for skill_lv, (action_id, ability_id) in enumerate(zipped_ids, start=1):
            hit_data_list: HitDataList = self._get_hit_data_lv(hit_data_cls, skill_lv, action_id, ability_id)

            if not hit_data_list:
                # No hit attribute data available, terminate further discovery
                break

            for hit_data in hit_data_list:
                # Create an empty array for the corresonding skill level
                if skill_lv > len(hit_data_mtx):
                    hit_data_mtx.append([])

                # Check if the criteria of getting the damaging hits or not meets
                if hit_data.hit_attr.deals_damage == deals_damage:
                    hit_data_mtx[skill_lv - 1].append(hit_data)

        if not any(hit_data for hit_data in hit_data_mtx):
            # No hit data available
            raise HitDataUnavailableError()

        return skill_data, hit_data_mtx

    def transform_supportive(self, skill_id: int, max_lv: int = 0) -> SupportiveSkillData:
        """
        Transform skill of ``skill_id`` to :class:`SupportiveSkillData`.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        :raises SkillDataNotFoundError: if the skill data is not found
        :raises ActionDataNotFoundError: if the action data file of the skill is not found
        :raises HitDataUnavailableError: if no hit data available
        """
        skill_data, hit_data_mtx = self.get_hit_data_matrix(skill_id, BuffingHitData,
                                                            deals_damage=False, max_lv=max_lv)

        return SupportiveSkillData(
            skill_data_raw=skill_data,
            hit_data_mtx=hit_data_mtx,
            action_condition_asset=self._action_cond
        )

    def transform_attacking(self, skill_id: int, max_lv: int = 0) -> AttackingSkillData:
        """
        Transform skill of ``skill_id`` to :class:`AttackingSkillDataEntry`.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        :raises SkillDataNotFoundError: if the skill data is not found
        :raises ActionDataNotFoundError: if the action data file of the skill is not found
        :raises HitDataUnavailableError: if no hit data available
        """
        skill_data, hit_data_mtx = self.get_hit_data_matrix(skill_id, DamagingHitData, max_lv=max_lv)

        return AttackingSkillData(
            skill_data_raw=skill_data,
            hit_data_mtx=hit_data_mtx,
            action_info_asset=self._action_info
        )
