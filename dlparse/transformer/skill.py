"""Skill data transformer."""
from typing import Optional, Iterable, TypeVar, Type

from dlparse.enums import HitExecType
from dlparse.errors import SkillDataNotFoundError, HitDataUnavailableError
from dlparse.model import HitData, AttackingSkillData, SupportiveSkillData, DamagingHitData, BuffingHitData
from dlparse.mono.asset import SkillDataAsset, SkillDataEntry, HitAttrEntry, HitAttrAsset, ActionConditionAsset
from dlparse.mono.loader import PlayerActionFileLoader

__all__ = ("SkillTransformer",)

T = TypeVar("T", bound=HitData)


class SkillTransformer:
    """Class to transform the skill data."""

    def __init__(self, skill_data_asset: SkillDataAsset, hit_attr_asset: HitAttrAsset,
                 action_condition_asset: ActionConditionAsset, action_loader: PlayerActionFileLoader):
        self._skill_data = skill_data_asset
        self._hit_attr = hit_attr_asset
        self._action_cond = action_condition_asset
        self._action_loader = action_loader

    def get_hit_data_matrix(self, skill_id: int, hit_data_cls: Type[T],
                            hit_exec_type: Optional[Iterable[HitExecType]] = None, /,
                            damage_hit_only: bool = True) \
            -> tuple[SkillDataEntry, list[list[T]]]:
        """
        Get a matrix of the hit data.

        The first index of the matrix is the skill level (Skill level 1 = index 0).

        If ``hit_exec_type`` is given, only the hit attributes that matches the given exec type will return.
        If the type does not match, the entry will be taken out.

        :raises SkillDataNotFoundError: skill data not found
        :raises ActionDataNotFoundError: action file not found
        :raises HitDataUnavailableError: no hit data available
        """
        # Get the skill data
        skill_data: Optional[SkillDataEntry] = self._skill_data.get_data_by_id(skill_id)
        if not skill_data:
            raise SkillDataNotFoundError(skill_id)

        # Get hit attribute data
        hit_data_mtx: list[list[DamagingHitData]] = []

        for skill_lv, action_id in enumerate(skill_data.action_id_1_by_level, start=1):
            for hit_label, action_component in self._action_loader.get_prefab(action_id).get_hit_actions(skill_lv):
                # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
                # pylint: disable=superfluous-parens
                hit_attr_data: Optional[HitAttrEntry]
                if not (hit_attr_data := self._hit_attr.get_data_by_id(hit_label)):
                    # No further skill data available
                    break

                hit_data = hit_data_cls(hit_attr=hit_attr_data, action_component=action_component)

                # Create an empty array for the corresonding skill level
                if skill_lv > len(hit_data_mtx):
                    hit_data_mtx.append([])

                # Check if exec type limitation meets
                meet_exec_type = not hit_exec_type or hit_attr_data.hit_exec_type in hit_exec_type
                # Check if damage dealing hits limitation meets
                meet_damage_only = not damage_hit_only or hit_data.hit_attr.deals_damage

                if meet_exec_type and meet_damage_only:
                    hit_data_mtx[skill_lv - 1].append(hit_data)

        if not any(hit_data for hit_data in hit_data_mtx):
            # No hit data available
            raise HitDataUnavailableError()

        return skill_data, hit_data_mtx

    def transform_supportive(self, skill_id: int) -> SupportiveSkillData:
        """Transform skill of ``skill_id`` to :class:`SupportiveSkillData`."""
        skill_data, hit_data_mtx = self.get_hit_data_matrix(skill_id, BuffingHitData,
                                                            {HitExecType.BUFF, HitExecType.GAUGE_REFILL},
                                                            damage_hit_only=False)

        return SupportiveSkillData(
            skill_data_raw=skill_data,
            hit_data_mtx=hit_data_mtx,
            action_condition_asset=self._action_cond
        )

    def transform_attacking(self, skill_id: int) -> AttackingSkillData:
        """
        Transform skill of ``skill_id`` to :class:`AttackingSkillDataEntry`.

        :raises SkillDataNotFoundError: if the skill data is not found
        :raises ActionDataNotFoundError: if the action data file of the skill is not found
        :raises HitDataUnavailableError: if no hit data available
        """
        skill_data, hit_data_mtx = self.get_hit_data_matrix(skill_id, DamagingHitData, {HitExecType.DAMAGE})

        return AttackingSkillData(
            skill_data_raw=skill_data,
            hit_data_mtx=hit_data_mtx
        )
