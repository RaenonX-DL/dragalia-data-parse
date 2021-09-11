"""Prefab file class for getting the components."""
import re
from typing import Optional, TextIO, Type, TypeVar

from dlparse.mono.asset.base import (
    ActionAssetBase, ActionComponentBase, ActionComponentHasHitLabels, ActionParserBase,
)
from dlparse.utils import get_hit_label_data, make_hit_label
from .buff_bomb import ActionBuffBomb
from .buff_field import ActionBuffField
from .bullet import ActionBullet
from .bullet_butterfly import ActionBulletButterfly
from .bullet_format import ActionBulletFormation
from .bullet_multi import ActionBulletMulti
from .bullet_parabola import ActionBulletParabola
from .bullet_pivot import ActionBulletPivot
from .bullet_stock_fire import ActionBulletStockFire
from .cancel import ActionActiveCancel
from .hit import ActionHit
from .motion import ActionMotion
from .set_hit import ActionSettingHit
from .terminate import ActionTerminateOthers

__all__ = ("PlayerActionPrefab",)

T = TypeVar("T", bound=ActionComponentBase)


class PlayerActionParser(ActionParserBase):
    """Player action prefab file parser."""

    SCRIPT_KEY: str = "$Script"

    SCRIPT_CLASS: dict[str, Type[T]] = {
        # Hits coming from the user themselves
        "ActionPartsHit": ActionHit,
        # Projectile hits
        "ActionPartsBullet": ActionBullet,
        "ActionPartsPivotBullet": ActionBulletPivot,
        "ActionPartsMultiBullet": ActionBulletMulti,
        "ActionPartsFireStockBullet": ActionBulletStockFire,
        "ActionPartsFormationBullet": ActionBulletFormation,
        "ActionPartsParabolaBullet": ActionBulletParabola,
        "ActionPartsButterflyBullet": ActionBulletButterfly,
        # Active actions
        "ActionPartsActiveCancel": ActionActiveCancel,
        "ActionPartsTerminateOtherParts": ActionTerminateOthers,
        # Any other hits
        "ActionPartsSettingHit": ActionSettingHit,
        "ActionPartsBuffFieldAttachment": ActionBuffField,
        "ActionPartsRemoveBuffTriggerBomb": ActionBuffBomb,
        # Non-hitting action parts
        "ActionPartsMotion": ActionMotion
    }

    @classmethod
    def parse_file(cls, file_like: TextIO) -> list[T]:
        components_raw: list[dict] = cls.get_components(file_like)
        components: list[T] = []

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

    def __init__(self, action_id: int, file_location: str):
        super().__init__(PlayerActionParser, file_location)

        # Properties
        self.action_id = action_id

        # Pre-categorize components for faster access
        self._damaging_hits: list[ActionComponentHasHitLabels] = [
            component for component in self if isinstance(component, ActionComponentHasHitLabels)
        ]
        self._cancel_actions: list[ActionActiveCancel] = [
            component for component in self if isinstance(component, ActionActiveCancel)
        ]
        self._terminate_others: Optional[ActionTerminateOthers] = next(
            (component for component in self if isinstance(component, ActionTerminateOthers)),
            None
        )
        self._motions: list[ActionMotion] = [
            component for component in self if isinstance(component, ActionMotion)
        ]

    def get_hit_actions(self, skill_lv: int = None) -> list[tuple[str, ActionComponentHasHitLabels]]:
        """
        Get a list of effective hitting actions in tuple ``(label name, action component)``.

        Specify ``skill_lv`` as ``None``, to get un-leveled hit actions.

        .. note::
            Each component contains hit label(s) which each of them corresponds to a hit attribute.
        """
        hit_actions: list[tuple[str, ActionComponentHasHitLabels]] = []

        # Sort hitting components by its starting time
        for action_hit in sorted(self._damaging_hits, key=lambda component: component.time_start):
            for hit_label in filter(self.is_effective_label, action_hit.hit_labels):  # Effective labels only
                hit_label_data = get_hit_label_data(hit_label)

                if (
                        action_hit.use_same_component
                        or not action_hit.use_same_component and hit_label_data.level == skill_lv
                ):
                    hit_actions.append((
                        make_hit_label(hit_label_data.original, level=skill_lv) if skill_lv else hit_label,
                        action_hit
                    ))

        return hit_actions

    @property
    def component_cancel_to_next(self) -> Optional[ActionTerminateOthers]:
        """
        Get the component indicating if the next action should be executed instead if the action cancels the others.

        Return ``None`` if not applicable.
        """
        return self._terminate_others

    @property
    def cancel_actions(self) -> list[ActionActiveCancel]:
        """Get a list of active cancel action components."""
        return self._cancel_actions

    @property
    def motions(self) -> list[ActionMotion]:
        """Sort the motions by its starting time, then return it as a list."""
        return list(sorted(self._motions, key=lambda motion: motion.time_start))

    @classmethod
    def is_effective_label(cls, label: str) -> bool:
        """Check if the label is an effective hitting label."""
        return bool(re.match(f"(?!{'|'.join(cls.omitted_label_starts)})", label))
