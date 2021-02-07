"""Skill data transformer."""
from dataclasses import dataclass, field
from typing import Iterable, Optional, TYPE_CHECKING, Type, TypeVar

from dlparse.enums import Condition, ConditionCategories, ConditionComposite
from dlparse.errors import (
    ActionInfoNotFoundError, CharaDataNotFoundError, HitDataUnavailableError, SkillDataNotFoundError,
)
from dlparse.model import (
    AttackingSkillData, BuffingHitData, DamagingHitData, HitData, SkillCancelActionUnit, SupportiveSkillData,
)
from dlparse.mono.asset import (
    ActionConditionEntry, CharaDataEntry, HitAttrEntry, SkillDataEntry, SkillReverseSearchResult,
)
from dlparse.mono.asset.base import ActionComponentHasHitLabels

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("SkillHitData", "SkillTransformer")

T = TypeVar("T", bound=HitData)
AT = TypeVar("AT", bound=ActionComponentHasHitLabels)

HitDataList = list[T]


@dataclass
class SkillHitData:
    """Hit data of a skill in various level."""

    hit_data: list[list[T]]
    # ``hit_count`` should exclude:
    # - dummy hit count as they requires the actual condition used to get the skill data
    # - hits with hit condition as they indirectly requires the actual condition same as above
    hit_count: list[int]

    rev_result: SkillReverseSearchResult
    skill_data: SkillDataEntry

    max_level: int

    chara_data: CharaDataEntry = field(init=False)

    def __post_init__(self):
        self.chara_data = self.rev_result.chara_data

        self.hit_data = self.hit_data[:self.max_level]
        self.hit_count = self.hit_count[:self.max_level]


class SkillTransformer:
    """Class to transform the skill data."""

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_manager = asset_manager

        self._asset_ability = asset_manager.asset_ability_data
        self._asset_action_cond = asset_manager.asset_action_cond
        self._asset_buff_count = asset_manager.asset_buff_count
        self._asset_chara_data = asset_manager.asset_chara_data
        self._asset_dragon_data = asset_manager.asset_dragon_data
        self._asset_hit_attr = asset_manager.asset_hit_attr
        self._asset_action_info_player = asset_manager.asset_action_info_player
        self._asset_skill = asset_manager.asset_skill_data

        self._loader_action = asset_manager.loader_action
        self._loader_chara_motion = asset_manager.loader_chara_motion
        self._loader_dragon_motion = asset_manager.loader_dragon_motion

    def _get_hit_data_from_hit_attr(
            self, hit_data_cls: Type[T], action_id: int, ability_ids: list[int],
            action_component: AT, hit_attr_data: HitAttrEntry, pre_condition: ConditionComposite
    ) -> HitDataList:
        ret: HitDataList = [hit_data_cls(
            hit_attr=hit_attr_data, action_component=action_component,
            action_id=action_id, pre_condition_comp=pre_condition,
            ability_data=[self._asset_ability.get_data_by_id(ability_id) for ability_id in ability_ids]
        )]

        if not hit_attr_data.has_action_condition:
            # Hit attribute does not have action condition, no post-processing needed
            return ret

        # Check for leveled action condition
        cur_ac: ActionConditionEntry = self._asset_action_cond.get_data_by_id(hit_attr_data.action_condition_id)
        lv_pre_cond_iter = iter(sorted(ConditionCategories.self_action_cond_lv.members))

        if not cur_ac.is_leveled:
            # Action condition not leveled, no further level discovery needed
            return ret

        # --- Leveled action condition discovery

        # Inject the precondition for the first level
        ret[0].pre_condition_comp += next(lv_pre_cond_iter)

        # Discover the next level of the action condition and return it until the highest level
        while cur_ac.level_up_id:
            cur_ac = self._asset_action_cond.get_data_by_id(cur_ac.level_up_id)

            ret.append(hit_data_cls(
                hit_attr=hit_attr_data, action_component=action_component,
                action_id=action_id, pre_condition_comp=pre_condition + next(lv_pre_cond_iter),
                ability_data=[self._asset_ability.get_data_by_id(ability_id) for ability_id in ability_ids],
                # Override action condition ID for later use
                action_cond_override=cur_ac.id
            ))

        return ret

    def _get_hit_data_action_component(
            self, hit_data_cls: Type[T], skill_lv: int, action_id: int, ability_ids: list[int], /,
            additional_pre_condition: Condition = Condition.NONE
    ) -> HitDataList:
        ret: HitDataList = []

        prefab = self._loader_action.get_prefab(action_id)

        # Convert hit actions of ``action_id`` to hit data
        for hit_label, action_component in prefab.get_hit_actions(skill_lv):
            pre_condition: ConditionComposite = ConditionComposite(additional_pre_condition)

            if action_component.skill_pre_condition:
                pre_condition += action_component.skill_pre_condition

            # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
            # pylint: disable=superfluous-parens
            if not (hit_attr_data := self._asset_hit_attr.get_data_by_id(hit_label)):
                # Hit attribute missing, skip it
                # - Not letting it "explode" because officials love to insert unused dummy data
                continue

            ret.extend(self._get_hit_data_from_hit_attr(
                hit_data_cls, action_id, ability_ids, action_component, hit_attr_data, pre_condition
            ))

        # Convert hit actions of the next action if the current one is being terminated
        # Formal Joachim S1 (`109503011`) has this
        if prefab.component_cancel_to_next:
            next_action_id = self._asset_action_info_player.get_data_by_id(action_id).next_action_id

            ret.extend(self._get_hit_data_action_component(
                hit_data_cls, skill_lv, next_action_id, ability_ids,
                additional_pre_condition=prefab.component_cancel_to_next.effective_condition.skill_pre_condition
            ))

        return ret

    def _get_hit_data_next_action(
            self, hit_data_cls: Type[T], skill_lv: int, action_id: int, ability_ids: list[int]
    ) -> HitDataList:
        # This currently handles additional inputs (Ramona S1, Lathna S1) only
        action_info = self._asset_action_info_player.get_data_by_id(action_id)
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
            curr_action_info = self._asset_action_info_player.get_data_by_id(curr_action_id)
            if not curr_action_info:
                raise ActionInfoNotFoundError(curr_action_id)

            prev_action_info = action_info_prev.pop(0)

            # Parse the actions and attach it to the hit data list to be returned
            if prev_action_info.max_addl_input_count:
                # Additional inputs available, list them all
                pre_conditions = [
                    ConditionCategories.skill_addl_inputs.convert_reversed(addl_input_count)
                    for addl_input_count in range(1, prev_action_info.max_addl_input_count + 1)
                ]
            elif prev_action_info.is_action_counter:
                pre_conditions = [Condition.COUNTER_RED_ATTACK]
            else:
                # Additional inputs unavailable, have one dummy pre-condition to trigger the parse
                pre_conditions = [Condition.NONE]

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
                    pre_condition_comp=ability_data.condition.to_condition_comp(),
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

    def _get_chara_skill_data(self, skill_id: int) -> tuple[SkillReverseSearchResult, SkillDataEntry]:
        """
        Get the skill reverse search result (containing chara data found) and the skill data of ``skill_id``.

        :raises SkillDataNotFoundError: if the skill data of `skill_id` is not found
        """
        # Get the character data
        rev_result: Optional[SkillReverseSearchResult] = self._asset_chara_data.get_chara_data_by_skill_id(
            self._asset_manager, skill_id
        )
        if not rev_result:
            skill_error = SkillDataNotFoundError(skill_id)
            chara_error = CharaDataNotFoundError(int(str(skill_id)[:-1]), "(Chara ID guessed from skill ID)")

            raise skill_error from chara_error

        # Get the skill data
        skill_data: Optional[SkillDataEntry] = self._asset_skill.get_data_by_id(skill_id)
        if not skill_data:
            raise SkillDataNotFoundError(skill_id)

        return rev_result, skill_data

    @staticmethod
    def _get_highest_skill_level(hit_data_mtx: list[list[HitData]]) -> int:
        """
        Get the highest level where the skill hit data is available.

        :raises HitDataUnavailableError: if no hit data is available across all levels
        """
        max_level = -1

        for level, hit_data_lv in enumerate(hit_data_mtx):
            if not hit_data_lv:
                continue

            max_level = max(max_level, level)

        if max_level == -1:
            # No hit data available at all levels
            raise HitDataUnavailableError()

        return max_level + 1

    @staticmethod
    def _get_zipped_ids(skill_data: SkillDataEntry, max_lv: int = 0) -> Iterable[tuple[int, int]]:
        """Get the zipped action ID 1 and ability ID of ``skill_data``."""
        if max_lv:
            # Limit the count of IDs can be zipped if ``max_lv`` is given
            return list(zip(skill_data.action_id_1_by_level, skill_data.ability_id_by_level))[:max_lv]

        # No ``max_lv`` given, return all possiblities
        return zip(skill_data.action_id_1_by_level, skill_data.ability_id_by_level)

    def get_skill_hit_data(
            self, skill_id: int, hit_data_cls: Type[T], /,
            effective_to_enemy: bool = True, max_lv: int = 0, ability_ids: Optional[list[int]] = None
    ) -> SkillHitData:
        """
        Get the hit data of a skill.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        ``ability_ids`` are the ability IDs to be additionally considered when parsing the skills.
        When the user enhance their skills via the character ability, this will be required to get the accurate result.

        The first index of the matrix is the skill level (Skill level 1 = index 0).

        :raises SkillDataNotFoundError: skill data not found
        :raises CharaDataNotFoundError: chara data not found
        :raises ActionDataNotFoundError: action file not found
        :raises HitDataUnavailableError: no hit data available
        """
        rev_result, skill_data = self._get_chara_skill_data(skill_id)

        if not ability_ids:
            ability_ids = []

        # Get hit attribute data
        hit_data_mtx: list[list[T]] = []
        hit_count: list[int] = []

        # Get all hit labels at different skill level
        for skill_lv, (action_id, ability_id) in enumerate(self._get_zipped_ids(skill_data, max_lv), start=1):
            hit_data_lv: HitDataList = self._get_hit_data_lv(
                hit_data_cls, skill_lv, action_id, [abid for abid in [ability_id] + ability_ids if abid]
            )

            # Create an empty array for the current skill level
            if skill_lv > len(hit_data_mtx):
                hit_data_mtx.append([])
                hit_count.append(0)

            for hit_data in hit_data_lv:
                # Count the base hit count
                # ------------------------
                # Dummy hit count should be counted with the actual condition,
                # therefore checking if the hit attribute is dummy hit count.
                # ------------------------
                # Hits with hit condition should not be counted as the base hit count.
                if not hit_data.hit_attr.dummy_hit_count and not hit_data.hit_attr.has_hit_condition:
                    hit_count[skill_lv - 1] += hit_data.get_hit_count(
                        hit_count[skill_lv - 1], ConditionComposite(), self._asset_manager
                    )

                # Check if the hit is effective to target, if desired
                # Check the docs of `hit_data.is_effective_to_enemy()` for the definition of effective
                if hit_data.is_effective_to_enemy(effective_to_enemy) == effective_to_enemy:
                    hit_data_mtx[skill_lv - 1].append(hit_data)

        return SkillHitData(
            hit_data=hit_data_mtx, hit_count=hit_count, max_level=self._get_highest_skill_level(hit_data_mtx),
            rev_result=rev_result, skill_data=skill_data,
        )

    def get_skill_cancel_unit_matrix(
            self, skill_hit_data: SkillHitData, max_lv: int = 0
    ) -> list[list[SkillCancelActionUnit]]:
        """
        Get the matrix of skill cancel action units.

        If ``skill_hit_data`` is a dragon skill, unique dragon binded to the character data of ``skill_hit_data``
        will be used to get the skill cancel actions.

        If the character data of ``skill_hit_data`` does not have a unique dragon,
        """
        cancel_units: list[list[SkillCancelActionUnit]] = []

        action_ids = skill_hit_data.skill_data.action_id_1_by_level
        if max_lv:
            action_ids = action_ids[:max_lv]

        for action_id in action_ids:
            prefab = self._loader_action.get_prefab(action_id)

            if skill_hit_data.rev_result.skill_id_entry.skill_num.is_dragon_skill:
                cancel_units.append(SkillCancelActionUnit.from_player_action_prefab(
                    self._loader_dragon_motion, skill_hit_data.chara_data.get_dragon_data(self._asset_dragon_data),
                    prefab
                ))
            else:
                cancel_units.append(SkillCancelActionUnit.from_player_action_prefab(
                    self._loader_chara_motion, skill_hit_data.chara_data, prefab
                ))

        return cancel_units

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
        :raises HitDataUnavailableError: if no hit data is available
        """
        skill_hit_data = self.get_skill_hit_data(
            skill_id, BuffingHitData,
            effective_to_enemy=False, max_lv=max_lv, ability_ids=ability_ids
        )

        return SupportiveSkillData(
            asset_manager=self._asset_manager,
            skill_hit_data=skill_hit_data
        )

    def transform_attacking(
            self, skill_id: int, /,
            max_lv: int = 0, ability_ids: Optional[list[int]] = None, is_exporting: bool = True
    ) -> AttackingSkillData:
        """
        Transform skill of ``skill_id`` to :class:`AttackingSkillDataEntry`.

        ``max_lv`` limits max skill level to be returned.
        If set to ``0``, all possible levels (max 4) will be returned.

        ``ability_ids`` are the ability IDs to be additionally considered when parsing the skills.
        When the user enhance their skills via the character ability, this will be required to get the accurate result.

        If ``is_exporting`` is ``True``, sectioned conditions will not be considered as a possible condition.
        This should be ``True`` when exporting the data to save the data size.

        Setting this to ``False`` can give you a quick overview of the skill,
        if iterating through all the possible conditions.

        :raises SkillDataNotFoundError: if the skill data is not found
        :raises ActionDataNotFoundError: if the action data file of the skill is not found
        :raises HitDataUnavailableError: if no hit data is available
        """
        skill_hit_data = self.get_skill_hit_data(
            skill_id, DamagingHitData, max_lv=max_lv, ability_ids=ability_ids
        )

        ret: AttackingSkillData = AttackingSkillData(
            asset_manager=self._asset_manager,
            skill_hit_data=skill_hit_data,
            is_exporting=is_exporting,
            cancel_unit_mtx=self.get_skill_cancel_unit_matrix(skill_hit_data, max_lv)
        )

        if not any(entry.has_effects_on_enemy for entry in ret.get_all_possible_entries()):
            # All effects does not target enemy at all level
            raise HitDataUnavailableError()

        return ret
