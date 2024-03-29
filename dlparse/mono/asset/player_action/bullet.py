"""Class for ``ActionPartsBullet`` action component."""
from dataclasses import dataclass
from typing import Any

# Intended to avoid circular import
# pylint: disable=consider-using-from-import
import dlparse.mono.asset as asset

__all__ = ("ActionBullet",)

COLLISION_INTERVAL_INEFFECTIVE = 50
"""Sentinel value indicating that collision interval is not applicable."""


@dataclass
class ActionBullet(asset.ActionComponentHasHitLabels):
    """Class of ``ActionPartsBullet`` component in the player action asset."""

    bullet_duration: float
    """
    Bullet lifetime in seconds.

    If this is ``0``, max hit count will be 0, indicating that max hitting count is not applicable.
    """
    collision_interval: float
    """Minimum interval for hitting the same enemy in seconds."""
    attenuation_rate: float = 1
    """
    Damage rate change for each hit. A value of 0.55 (Yukata unmasked S1) means the next damage will be 0.55x.

    Hits that do not deteriorate will have this set to ``1``.
    """

    @property
    def max_hit_count(self) -> int:
        """Maximum count of hits possible. ``0`` means not applicable."""
        if not self.collision_interval or self.collision_interval == COLLISION_INTERVAL_INEFFECTIVE:
            return 0

        hit_count = int(self.bullet_duration // self.collision_interval)

        if self.bullet_duration % self.collision_interval:
            hit_count += 1

        return hit_count

    @property
    def will_deteriorate(self) -> bool:
        """Check if the bullet will deteriorate after hitting an enemy."""
        return self.attenuation_rate != 1.0

    @classmethod
    def get_base_kwargs(cls, raw_data: dict[str, Any]) -> dict[str, Any]:
        base_kwargs = super().get_base_kwargs(raw_data)

        # Bullet configurations
        if "_bulletDuration" in raw_data:
            base_kwargs["bullet_duration"] = raw_data["_bulletDuration"]
        if "_attenuationRate" in raw_data:
            base_kwargs["attenuation_rate"] = raw_data["_attenuationRate"]
        if "_collisionHitInterval" in raw_data:
            base_kwargs["collision_interval"] = raw_data["_collisionHitInterval"]

        return base_kwargs

    @classmethod
    def parse_raw(cls, data: asset.ActionComponentData) -> "ActionBullet":
        kwargs = cls.get_base_kwargs(data)

        # Main hit labels
        labels_possible: list[str] = [data["_hitAttrLabel"]] + data["_hitAttrLabelSubList"]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            arrange_bullet: asset.ActionBulletArranged = asset.ActionBulletArranged.parse_raw(data["_arrangeBullet"])

            # If max hit count available (arrange bullet has duration), extend hit labels to match the hit count
            labels_possible.extend(arrange_bullet.hit_labels * (arrange_bullet.max_hit_count or 1))

        if kwargs["loop_data"]:  # This will be `None` if inapplicable
            labels_possible *= (1 + kwargs["loop_data"].loop_count)  # `1` for the original execution

        return ActionBullet(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
