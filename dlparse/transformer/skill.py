"""Skill data transformer."""
from typing import Optional, TYPE_CHECKING, Type, TypeVar

from dlparse.enums import SkillCondition, SkillConditionCategories
from dlparse.errors import ActionInfoNotFoundError, AppValueError, HitDataUnavailableError, SkillDataNotFoundError
from dlparse.model import AttackingSkillData, BuffingHitData, DamagingHitData, HitData, SupportiveSkillData
from dlparse.mono.asset import SkillDataAsset, SkillDataEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("SkillTransformer",)

T = TypeVar("T", bound=HitData)

HitDataList = list[T]


class SkillTransformer:
    """Class to transform the skill data."""

    def __init__(self, asset_manager: "AssetManager"):
        self._skill_data = asset_manager.asset_skill
        self._hit_attr = asset_manager.asset_hit_attr
        self._action_cond = asset_manager.asset_action_cond
        self._action_loader = asset_manager.loader_pa
        self._action_info = asset_manager.asset_pa_info
        self._ability_asset = asset_manager.asset_ability_data

    @property
    def skill_data_asset(self) -> SkillDataAsset:
        """Get the skill data asset used by this transformer."""
        return self._skill_data

    def _get_hit_data_action_component(
            self, hit_data_cls: Type[T], skill_lv: int, action_id: int, /,
            additional_pre_condition: SkillCondition = SkillCondition.NONE
    ) -> HitDataList:
        ret: HitDataList = []

        for hit_label, action_component in self._action_loader.get_prefab(action_id).get_hit_actions(skill_lv):
            # Check for multiple pre-conditions, raise error if needed
            if additional_pre_condition and action_component.condition_data.skill_pre_condition:
                raise AppValueError(f"Multiple pre-condition detected: "
                                    f"{additional_pre_condition} "
                                    f"& {action_component.condition_data.skill_pre_condition}")

            pre_condition = additional_pre_condition or action_component.condition_data.skill_pre_condition

            # If the hit attribute is missing, just skip it; sometimes it's simply missing
            if hit_attr_data := self._hit_attr.get_data_by_id(hit_label):
                ret.append(hit_data_cls(hit_attr=hit_attr_data, action_component=action_component,
                                        action_id=action_id, pre_condition=pre_condition))

        return ret

    def _get_hit_data_next_action(self, hit_data_cls: Type[T], skill_lv: int, action_id: int) -> HitDataList:
        # This currently handles additional inputs (Ramona S1, Lathna S1) only
        ret: HitDataList = []

        action_info = self._action_info.get_data_by_id(action_id)
        if init_next_action_id := action_info.next_action_id:
            action_id_queue = [init_next_action_id]
            action_info_prev = [action_info]

            while action_id_queue:
                # Pop the next action ID to get the prefab and the info
                curr_action_id = action_id_queue.pop(0)
                curr_action_info = self._action_info.get_data_by_id(curr_action_id)
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
                    ret.extend(self._get_hit_data_action_component(hit_data_cls, skill_lv, curr_action_id,
                                                                   additional_pre_condition=pre_condition))

                # Add all next actions, if available
                if curr_action_info.next_action_id:
                    action_id_queue.append(curr_action_info.next_action_id)
                    action_info_prev.append(curr_action_info)

        return ret

    def _get_hit_data_lv_ability(self, hit_data_cls: Type[T], action_id: int, ability_id: int) -> HitDataList:
        ret: HitDataList = []

        if init_ability_data := self._ability_asset.get_data_by_id(ability_id):
            # Get all ability data from the ability chain
            ability_data_dict = init_ability_data.get_all_ability(self._ability_asset)

            # Loop through each hit labels of each ability data
            for ability_data in ability_data_dict.values():
                for hit_label in ability_data.assigned_hit_labels:
                    # If the hit attribute is missing, just skip it; sometimes it's simply missing
                    if hit_attr_data := self._hit_attr.get_data_by_id(hit_label):
                        # Parse to :class:`HitData` and attach it to the hit data list to be returned
                        ret.append(hit_data_cls(
                            hit_attr=hit_attr_data, action_component=None, action_id=action_id,
                            pre_condition=ability_data.condition.to_skill_condition()
                        ))

        return ret

    def _get_hit_data_lv(self, hit_data_cls: Type[T], skill_lv: int, action_id: int, ability_id: int) -> HitDataList:
        """Get a list of hit attributes at a certain ``skill_lv``."""
        ret: HitDataList = []

        ret.extend(self._get_hit_data_action_component(hit_data_cls, skill_lv, action_id))
        ret.extend(self._get_hit_data_next_action(hit_data_cls, skill_lv, action_id))
        ret.extend(self._get_hit_data_lv_ability(hit_data_cls, action_id, ability_id))

        return ret

    def get_hit_data_matrix(
            self, skill_id: int, hit_data_cls: Type[T], /,
            effective_to_enemy: bool = True, max_lv: int = 0
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
            hit_data_lv: HitDataList = self._get_hit_data_lv(hit_data_cls, skill_lv, action_id, ability_id)

            # Create an empty array for the current skill level
            if skill_lv > len(hit_data_mtx):
                hit_data_mtx.append([])

            for hit_data in hit_data_lv:
                # Check if the hit is effective to target, if desired; check the doc for the definition of effective
                if hit_data.hit_attr.is_effective_to_enemy(self._action_cond) == effective_to_enemy:
                    hit_data_mtx[skill_lv - 1].append(hit_data)

        if not any(hit_data for hit_data in hit_data_mtx):
            # No hit data available at all levels
            raise HitDataUnavailableError()

        highest_available_level = max(idx for idx, hit_data_lv in enumerate(hit_data_mtx) if hit_data_lv)

        return skill_data, hit_data_mtx[:highest_available_level + 1]

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
                                                            effective_to_enemy=False, max_lv=max_lv)

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
            asset_action_info=self._action_info,
            asset_action_cond=self._action_cond
        )
