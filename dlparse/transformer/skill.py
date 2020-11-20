"""Skill data transformer."""
from typing import Optional

from dlparse.errors import SkillDataNotFound, ActionDataNotFound
from dlparse.model import AttackingSkillData
from dlparse.mono.asset import SkillDataAsset, SkillDataEntry, HitAttrEntry, HitAttrAsset, PlayerActionPrefab
from dlparse.mono.path import PlayerActionFilePathFinder

__all__ = ("SkillTransformer",)


class SkillTransformer:
    """Class to transform the skill data."""

    SKILL_MAX_LV_ATK = 4
    """Currently known max level for attacking skills."""

    def __init__(self, skill_data_asset: SkillDataAsset, hit_attr_asset: HitAttrAsset,
                 action_path_finder: PlayerActionFilePathFinder):
        self._skill_data = skill_data_asset
        self._hit_attr = hit_attr_asset
        self._action_path = action_path_finder

    def transform_supportive(self, skill_id: int):
        """Transform skill of ``skill_id`` to :class:`SupportiveSkillData`."""
        raise NotImplementedError()

    def transform_attacking(self, skill_id: int) -> AttackingSkillData:
        """
        Transform skill of ``skill_id`` to :class:`AttackingSkillData`.

        :raises SkillDataNotFound: if the skill data is not found
        :raises ActionDataNotFound: if the action data file of the skill is not found
        """
        # Get the skill data
        skill_data: Optional[SkillDataEntry] = self._skill_data.get_data_by_id(skill_id)
        if not skill_data:
            raise SkillDataNotFound(skill_id)

        # Get the skill action data
        action_id = skill_data.action_1_id
        action_file_path = self._action_path.get_file_path(action_id)

        if not action_file_path:
            raise ActionDataNotFound(action_id, skill_id)

        # Get the skill action prefab data
        action_prefab = PlayerActionPrefab(action_file_path)

        # Get skill data
        hits: list[int] = []
        mods: list[list[float]] = []
        dmg_label: list[list[HitAttrEntry]] = []

        for hit_label_root in action_prefab.damage_dealing_hit_labels:
            for skill_lv in range(1, self.SKILL_MAX_LV_ATK + 1):
                hit_label = self._hit_attr.get_hit_label(hit_label_root, skill_lv)

                hit_attr_data: Optional[HitAttrEntry] = self._hit_attr.get_data_by_id(hit_label)
                if not hit_attr_data:
                    # No further skill data available
                    break

                mod = hit_attr_data.damage_modifier

                # Data to be attached to the model
                if hit_attr_data.deal_damage:
                    if skill_lv > len(mods):
                        mods.append([mod])
                        hits.append(1)
                        dmg_label.append([hit_attr_data])
                    else:
                        lv_index = skill_lv - 1

                        mods[lv_index].append(mod)
                        hits[lv_index] += 1
                        dmg_label[lv_index].append(hit_attr_data)

        return AttackingSkillData(
            hit_count=hits,
            mods=mods,
            damage_hit_attrs=dmg_label
        )
