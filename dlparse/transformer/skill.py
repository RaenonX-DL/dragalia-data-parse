"""Skill data transformer."""
from typing import Optional, TYPE_CHECKING, Type, TypeVar

from dlparse.enums import SkillCondition, SkillConditionCategories
from dlparse.errors import (
    ActionInfoNotFoundError, HitDataUnavailableError, PreconditionCollidedError, SkillDataNotFoundError,
)
from dlparse.model import AttackingSkillData, BuffingHitData, DamagingHitData, HitData, SupportiveSkillData
from dlparse.mono.asset import SkillDataEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("SkillTransformer",)

T = TypeVar("T", bound=HitData)

HitDataList = list[T]


class SkillTransformer:
    """Class to transform the skill data."""

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_skill = asset_manager.asset_skill_data
        self._asset_hit_attr = asset_manager.asset_hit_attr
        self._asset_action_cond = asset_manager.asset_action_cond
        self._loader_action = asset_manager.loader_action
        self._asset_pa_info = asset_manager.asset_pa_info
        self._asset_ability = asset_manager.asset_ability_data

    def _get_hit_data_action_component(
            self, hit_data_cls: Type[T], skill_lv: int, action_id: int, ability_ids: list[int], /,
            additional_pre_condition: SkillCondition = SkillCondition.NONE
    ) -> HitDataList:
        ret: HitDataList = []

        prefab = self._loader_action.get_prefab(action_id)

        # Convert hit actions of ``action_id`` to hit data
        for hit_label, action_component in prefab.get_hit_actions(skill_lv):
            # Check for multiple pre-conditions, raise error if needed
            if additional_pre_condition and action_component.skill_pre_condition:
                raise PreconditionCollidedError(additional_pre_condition, action_component.skill_pre_condition)

            pre_condition = additional_pre_condition or action_component.skill_pre_condition

            # If the hit attribute is missing, just skip it; sometimes it's simply missing
            if hit_attr_data := self._asset_hit_attr.get_data_by_id(hit_label):
                ret.append(hit_data_cls(
                    hit_attr=hit_attr_data, action_component=action_component,
                    action_id=action_id, pre_condition=pre_condition,
                    ability_data=[self._asset_ability.get_data_by_id(ability_id) for ability_id in ability_ids]
                ))

        # Convert hit actions of the next action if the current one is being terminated
        # Formal Joachim S1 (`109503011`) has this
        if prefab.component_cancel_to_next:
            next_action_id = self._asset_pa_info.get_data_by_id(action_id).next_action_id

            ret.extend(self._get_hit_data_action_component(
                hit_data_cls, skill_lv, next_action_id, ability_ids,
                additional_pre_condition=prefab.component_cancel_to_next.effective_condition.skill_pre_condition
            ))

        return ret

    def _get_hit_data_next_action(
            self, hit_data_cls: Type[T], skill_lv: int, action_id: int, ability_ids: list[int]
    ) -> HitDataList:
        # This currently handles additional inputs (Ramona S1, Lathna S1) only
        action_info = self._asset_pa_info.get_data_by_id(action_id)
        if not action_info.next_action_id:
            # No next action
            return []

        if self._loader_action.get_prefab(action_id).component_cancel_to_next:
            # Next action only procs if it's canceled by ``action_id``
            # Handled in ``_get_hit_data_action_component()``
            return []

        ret: HitDataList = []

        action_id_queue = [action_info.next_action_id]
        action_info_prev = [action_info]

        while action_id_queue:
            # Pop the next action ID to get the prefab and the info
            curr_action_id = action_id_queue.pop(0)
            curr_action_info = self._asset_pa_info.get_data_by_id(curr_action_id)
            if not curr_action_info:
                raise ActionInfoNotFoundError(curr_action_id)

            prev_action_info = action_info_prev.pop(0)

            # Parse the actions and attach it to the hit data list to be returned
            if prev_action_info.max_addl_input_count:
                # Additional inputs available, list them all
                pre_conditions = [
                    SkillConditionCategories.skill_addl_inputs.convert_reversed(addl_input_count)
                    for addl_input_count in range(1, prev_action_info.max_addl_input_count + 1)
                ]
            else:
                # Additional inputs unavailable, have one dummy pre-condition to trigger the parse
                pre_conditions = [SkillCondition.NONE]

            # Iterate through all possible pre-conditions
            for pre_condition in pre_conditions:
                ret.extend(self._get_hit_data_action_component(
                    hit_data_cls, skill_lv, curr_action_id, ability_ids, additional_pre_condition=pre_condition
                ))

            # Add all next actions, if available
            if curr_action_info.next_action_id:
                action_id_queue.append(curr_action_info.next_action_id)
                action_info_prev.append(curr_action_info)

        return ret

    def _get_hit_data_lv_ability_to_others(
            self, hit_data_cls: Type[T], action_id: int, ability_ids: list[int]
    ) -> HitDataList:
        """
        Get the other hit attributes linked to the ability.

        Note that this does **NOT** include the effects coming from the ability,
        for example, Mitsuhide S2 combo count damage boost.
        """
        ret: HitDataList = []

        for ability_id in ability_ids:
            # Get all ability data from the ability chain
            ability_data_dict = self._asset_ability.get_data_by_id(ability_id).get_all_ability(self._asset_ability)

            # Get all hit labels and its ability data
            ability_hit_labels = [
                (ability_data, hit_label) for ability_data in ability_data_dict.values()
                for hit_label in ability_data.assigned_hit_labels
            ]

            # Loop through each ability data
            for ability_data, hit_label in ability_hit_labels:
                # If the hit attribute is missing, just skip it; sometimes it's simply missing
                # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
                # pylint: disable=superfluous-parens
                if not (hit_attr_data := self._asset_hit_attr.get_data_by_id(hit_label)):
                    continue

                # Parse to :class:`HitData` and attach it to the hit data list to be returned
                ret.append(hit_data_cls(
                    hit_attr=hit_attr_data, action_component=None, action_id=action_id,
                    pre_condition=ability_data.condition.to_skill_condition(),
                    ability_data=[ability_data]
                ))

        return ret

    def _get_hit_data_lv(
            self, hit_data_cls: Type[T], skill_lv: int, action_id: int, ability_ids: list[int]
    ) -> HitDataList:
        """Get a list of hit attributes at a certain ``skill_lv``."""
        ret: HitDataList = []

        ret.extend(self._get_hit_data_action_component(hit_data_cls, skill_lv, action_id, ability_ids))
        ret.extend(self._get_hit_data_next_action(hit_data_cls, skill_lv, action_id, ability_ids))
        ret.extend(self._get_hit_data_lv_ability_to_others(hit_data_cls, action_id, ability_ids))

        return ret

    def get_hit_data_matrix(
            self, skill_id: int, hit_data_cls: Type[T], /,
            effective_to_enemy: bool = True, max_lv: int = 0, ability_ids: Optional[list[int]] = None
    ) -> tuple[SkillDataEntry, list[list[T]]]:
        """
        Get a matrix of the hit data.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        ``ability_ids`` are the ability IDs to be additionally considered when parsing the skills.
        When the user enhance their skills via the character ability, this will be required to get the accurate result.

        The first index of the matrix is the skill level (Skill level 1 = index 0).

        :raises SkillDataNotFoundError: skill data not found
        :raises ActionDataNotFoundError: action file not found
        :raises HitDataUnavailableError: no hit data available
        """
        # Get the skill data
        skill_data: Optional[SkillDataEntry] = self._asset_skill.get_data_by_id(skill_id)
        if not skill_data:
            raise SkillDataNotFoundError(skill_id)

        if not ability_ids:
            ability_ids = []

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
            hit_data_lv: HitDataList = self._get_hit_data_lv(
                hit_data_cls, skill_lv, action_id, [abid for abid in [ability_id] + ability_ids if abid]
            )

            # Create an empty array for the current skill level
            if skill_lv > len(hit_data_mtx):
                hit_data_mtx.append([])

            for hit_data in hit_data_lv:
                # Check if the hit is effective to target, if desired; check the docs for the definition of effective
                if hit_data.is_effective_to_enemy(self._asset_action_cond) == effective_to_enemy:
                    hit_data_mtx[skill_lv - 1].append(hit_data)

        if not any(hit_data for hit_data in hit_data_mtx):
            # No hit data available at all levels
            raise HitDataUnavailableError()

        highest_available_level = max(idx for idx, hit_data_lv in enumerate(hit_data_mtx) if hit_data_lv)

        return skill_data, hit_data_mtx[:highest_available_level + 1]

    def transform_supportive(
            self, skill_id: int, max_lv: int = 0, ability_ids: Optional[list[int]] = None
    ) -> SupportiveSkillData:
        """
        Transform skill of ``skill_id`` to :class:`SupportiveSkillData`.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        ``ability_ids`` are the ability IDs to be additionally considered when parsing the skills.
        When the user enhance their skills via the character ability, this will be required to get the accurate result.

        :raises SkillDataNotFoundError: if the skill data is not found
        :raises ActionDataNotFoundError: if the action data file of the skill is not found
        :raises HitDataUnavailableError: if no hit data available
        """
        skill_data, hit_data_mtx = self.get_hit_data_matrix(
            skill_id, BuffingHitData,
            effective_to_enemy=False, max_lv=max_lv, ability_ids=ability_ids
        )

        return SupportiveSkillData(
            skill_data_raw=skill_data,
            hit_data_mtx=hit_data_mtx,
            action_condition_asset=self._asset_action_cond
        )

    def transform_attacking(
            self, skill_id: int, /, max_lv: int = 0, ability_ids: Optional[list[int]] = None
    ) -> AttackingSkillData:
        """
        Transform skill of ``skill_id`` to :class:`AttackingSkillDataEntry`.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        ``ability_ids`` are the ability IDs to be additionally considered when parsing the skills.
        When the user enhance their skills via the character ability, this will be required to get the accurate result.

        :raises SkillDataNotFoundError: if the skill data is not found
        :raises ActionDataNotFoundError: if the action data file of the skill is not found
        :raises HitDataUnavailableError: if no hit data available
        """
        skill_data, hit_data_mtx = self.get_hit_data_matrix(
            skill_id, DamagingHitData, max_lv=max_lv, ability_ids=ability_ids
        )

        return AttackingSkillData(
            skill_data_raw=skill_data,
            hit_data_mtx=hit_data_mtx,
            asset_action_info=self._asset_pa_info,
            asset_action_cond=self._asset_action_cond
        )
