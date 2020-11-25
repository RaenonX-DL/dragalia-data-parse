"""Prefab file class for getting the components."""
import re
from typing import Type

from dlparse.mono.asset.base import (
    ActionAssetBase, ActionParserBase, ActionComponentBase, ActionComponentDamageDealer
)
from .bullet import ActionBullet
from .bullet_format import ActionBulletFormation
from .bullet_multi import ActionBulletMulti
from .bullet_parabola import ActionBulletParabola
from .bullet_stock import ActionBulletStock
from .hit import ActionHit

__all__ = ("PlayerActionPrefab",)


class PlayerActionParser(ActionParserBase):
    """Player action prefab file parser."""

    SCRIPT_KEY: str = "$Script"

    SCRIPT_CLASS: dict[str, Type[ActionComponentBase]] = {
        "ActionPartsHit": ActionHit,
        "ActionPartsBullet": ActionBullet,
        "ActionPartsMultiBullet": ActionBulletMulti,
        "ActionPartsFireStockBullet": ActionBulletStock,
        "ActionPartsFormationBullet": ActionBulletFormation,
        "ActionPartsParabolaBullet": ActionBulletParabola
    }

    @classmethod
    def parse_file(cls, file_path: str) -> list[ActionComponentBase]:
        components_raw: list[dict] = cls.get_components(file_path)
        components: list[ActionComponentBase] = []

        for component in components_raw:
            component_class = cls.SCRIPT_CLASS.get(component.get(cls.SCRIPT_KEY))

            if not component_class:
                # No corresponding component class or no script key specified
                continue

            components.append(component_class.parse_raw(component["_data"]))

        return components


class PlayerActionPrefab(ActionAssetBase):
    """Class representing a single player action prefab file."""

    omitted_label_starts: set[str] = {
        "CMN_AVOID",
    }
    """List of label starting keywords to be omitted."""

    def __init__(self, file_path: str):
        super().__init__(PlayerActionParser, file_path)

        # Pre-categorize components for faster access
        self._damaging_hits: list[ActionComponentDamageDealer] = []

        for component in self:
            if isinstance(component, ActionComponentDamageDealer):
                self._damaging_hits.append(component)

    def get_hit_actions(self, skill_lv: int) -> list[tuple[str, ActionComponentDamageDealer]]:
        """
        Get a list of effective hitting actions in tuple ``(label name, action component)``.

        .. note::
            Each component contains hit label(s) which each of them corresponds to a hit attribute.
        """
        hit_actions: list[tuple[str, ActionComponentDamageDealer]] = []

        # Sort hitting components by its starting time
        for action_hit in sorted(self._damaging_hits, key=lambda component: component.time_start):
            for hit_label in filter(self.is_effective_label, action_hit.hit_labels):  # Effective labels only
                if (action_hit.use_same_component
                        or not action_hit.use_same_component and self.get_hit_label_skill_lv(hit_label) == skill_lv):
                    hit_actions.append((self.get_hit_label_at_skill_lv(hit_label, skill_lv), action_hit))

        return hit_actions

    @classmethod
    def is_effective_label(cls, label: str) -> bool:
        """Check if the label is an effective hitting label."""
        return bool(re.match(f"(?!{'|'.join(cls.omitted_label_starts)})", label))

    @staticmethod
    def get_hit_label_at_skill_lv(original_label: str, skill_lv: int) -> str:
        """
        Get the hit label at ``level``.

        For example, if ``original_label`` is ``SWD_110_04_H01_LV02`` and ``level`` is ``3``,
        the return will be ``SWD_110_04_H01_LV03``.
        """
        return original_label[:-1] + str(skill_lv)

    @staticmethod
    def get_hit_label_skill_lv(label: str) -> int:
        """Get the skill level of ``label``."""
        return int(label[-1])
