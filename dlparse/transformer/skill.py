"""Skill data transformer."""
from typing import Optional

from dlparse.enums import HitExecType
from dlparse.errors import SkillDataNotFound
from dlparse.model import AttackingSkillData
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
        # TODO: TBA - Supportive
        raise NotImplementedError()

    def get_hit_attr_matrix(self, skill_id: int, hit_exec_type: Optional[HitExecType] = None)\
            -> tuple[SkillDataEntry, list[list[HitAttrEntry]]]:
        """
        Get a matrix of the hit attributes.

        The first index of the matrix is the skill level (Skill level 1 = index 0).

        If ``hit_exec_type`` is given, only the hit attributes that matches the given exec type will return.
        If the type does not match, the entry will be taken out.

        :raises SkillDataNotFound: skill data not found
        """
        # Get the skill data
        skill_data: Optional[SkillDataEntry] = self._skill_data.get_data_by_id(skill_id)
        if not skill_data:
            raise SkillDataNotFound(skill_id)

        # Get hit attribute data
        hit_attr_mtx: list[list[HitAttrEntry]] = []

        for skill_lv, action_id in enumerate(skill_data.action_id_1_by_level, start=1):
            action_prefab = self._action_loader.get_prefab(action_id)

            for hit_label_root in action_prefab.effective_hit_labels:
                hit_label = self._hit_attr.get_hit_label(hit_label_root, skill_lv)

                hit_attr_data: Optional[HitAttrEntry] = self._hit_attr.get_data_by_id(hit_label)
                if not hit_attr_data:
                    # No further skill data available
                    break

                # Create an empty array for the corresonding skill level
                if skill_lv > len(hit_attr_mtx):
                    hit_attr_mtx.append([])

                if not hit_exec_type or (hit_exec_type and hit_attr_data.hit_exec_type == hit_exec_type):
                    hit_attr_mtx[skill_lv - 1].append(hit_attr_data)

        return skill_data, hit_attr_mtx

    def transform_attacking(self, skill_id: int) -> AttackingSkillData:
        """
        Transform skill of ``skill_id`` to :class:`AttackingSkillDataEntry`.

        :raises SkillDataNotFound: if the skill data is not found
        :raises ActionDataNotFound: if the action data file of the skill is not found
        """
        skill_data, hit_attr_mtx = self.get_hit_attr_matrix(skill_id, HitExecType.DAMAGE)

        skill_data: SkillDataEntry
        hit_attr_mtx: list[list[HitAttrEntry]]

        mods: list[list[float]] = []
        hits: list[int] = []

        for skill_lv, action_id in enumerate(skill_data.action_id_1_by_level, start=1):
            action_prefab = self._action_loader.get_prefab(action_id)

            for hit_label_root in action_prefab.effective_hit_labels:
                hit_label = self._hit_attr.get_hit_label(hit_label_root, skill_lv)

                hit_attr_data: Optional[HitAttrEntry] = self._hit_attr.get_data_by_id(hit_label)
                if not hit_attr_data:
                    # No further skill data available
                    break

                mod = hit_attr_data.damage_modifier

                if skill_lv > len(mods):
                    mods.append([])
                    hits.append(0)

                # Data to be attached to the model
                if hit_attr_data.deal_damage:
                    lv_index = skill_lv - 1

                    mods[lv_index].append(mod)
                    hits[lv_index] += 1

        return AttackingSkillData(
            skill_data_raw=skill_data,
            hit_count=hits,
            mods=mods,
            hit_attr_mtx=hit_attr_mtx
        )
