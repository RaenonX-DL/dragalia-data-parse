"""Skill data transformer."""
from typing import Optional

from dlparse.enums import HitExecType
from dlparse.errors import SkillDataNotFoundError
from dlparse.model import AttackingSkillData, DamagingHitData
from dlparse.mono.asset import SkillDataAsset, SkillDataEntry, HitAttrEntry, HitAttrAsset
from dlparse.mono.loader import PlayerActionFileLoader

__all__ = ("SkillTransformer",)


class SkillTransformer:
    """Class to transform the skill data."""

    def __init__(self, skill_data_asset: SkillDataAsset, hit_attr_asset: HitAttrAsset,
                 action_loader: PlayerActionFileLoader):
        self._skill_data = skill_data_asset
        self._hit_attr = hit_attr_asset
        self._action_loader = action_loader

    def transform_supportive(self, skill_id: int):
        """Transform skill of ``skill_id`` to :class:`SupportiveSkillData`."""
        # TODO: TBA - Supportive / Buffing
        raise NotImplementedError()

    def get_hit_data_matrix(self, skill_id: int, hit_exec_type: Optional[HitExecType] = None, /,
                            damage_hit_only: bool = True) \
            -> tuple[SkillDataEntry, list[list[DamagingHitData]]]:
        """
        Get a matrix of the single hit data.

        The first index of the matrix is the skill level (Skill level 1 = index 0).

        If ``hit_exec_type`` is given, only the hit attributes that matches the given exec type will return.
        If the type does not match, the entry will be taken out.

        :raises SkillDataNotFoundError: skill data not found
        :raises ActionDataNotFoundError: action file not found
        """
        # Get the skill data
        skill_data: Optional[SkillDataEntry] = self._skill_data.get_data_by_id(skill_id)
        if not skill_data:
            raise SkillDataNotFoundError(skill_id)

        # Get hit attribute data
        hit_data_mtx: list[list[DamagingHitData]] = []

        for skill_lv, action_id in enumerate(skill_data.action_id_1_by_level, start=1):
            action_prefab = self._action_loader.get_prefab(action_id)

            for hit_label, action_component in action_prefab.get_hit_actions(skill_lv):
                # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
                # pylint: disable=superfluous-parens
                hit_attr_data: Optional[HitAttrEntry]
                if not (hit_attr_data := self._hit_attr.get_data_by_id(hit_label)):
                    # No further skill data available
                    break

                hit_data = DamagingHitData(hit_attr=hit_attr_data, action_component=action_component)

                # Create an empty array for the corresonding skill level
                if skill_lv > len(hit_data_mtx):
                    hit_data_mtx.append([])

                # Check if exec type limitation meets
                meet_exec_type = not hit_exec_type or (hit_exec_type and hit_attr_data.hit_exec_type == hit_exec_type)
                # Check if damage dealing hits limitation meets
                meet_damage_only = not damage_hit_only or (damage_hit_only and hit_data.hit_attr.deal_damage)

                if meet_exec_type and meet_damage_only:
                    hit_data_mtx[skill_lv - 1].append(hit_data)

        return skill_data, hit_data_mtx

    def transform_attacking(self, skill_id: int) -> AttackingSkillData:
        """
        Transform skill of ``skill_id`` to :class:`AttackingSkillDataEntry`.

        :raises SkillDataNotFoundError: if the skill data is not found
        :raises ActionDataNotFoundError: if the action data file of the skill is not found
        """
        skill_data, hit_data_mtx = self.get_hit_data_matrix(skill_id, HitExecType.DAMAGE)

        return AttackingSkillData(
            skill_data_raw=skill_data,
            hit_data_mtx=hit_data_mtx
        )
