"""Prefab file class for getting the components."""
from typing import Type

from dlparse.mono.asset.base import (
    ActionAssetBase, ActionParserBase, ActionComponentBase, ActionComponentDamageDealerMixin
)
from .bullet import ActionBullet
from .hit import ActionHit

__all__ = ("PlayerActionPrefab",)


class PlayerActionParser(ActionParserBase):
    """Player action prefab file parser."""

    SCRIPT_KEY: str = "$Script"

    SCRIPT_CLASS: dict[str, Type[ActionComponentBase]] = {
        "ActionPartsHit": ActionHit,
        "ActionPartsBullet": ActionBullet
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

    def __init__(self, file_path: str):
        super().__init__(PlayerActionParser, file_path)

        # Pre-categorize components for faster access
        self._damaging_hits: list[ActionComponentDamageDealerMixin] = []

        for component in self:
            if isinstance(component, ActionComponentDamageDealerMixin):
                self._damaging_hits.append(component)

    @property
    def damage_dealing_hit_labels(self) -> list[str]:
        """
        Get a :class:`list` of damage dealing hit labels.

        Note that the damage dealing hit here may not actually deal damage. The hit could attack
        """
        return [
            hit_label for action_hit in sorted(self._damaging_hits, key=lambda component: component.time_start)
            for hit_label in action_hit.hit_labels
            if hit_label not in ActionComponentDamageDealerMixin.NON_DAMAGE_DEALING_LABELS
        ]
