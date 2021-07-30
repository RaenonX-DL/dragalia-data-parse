"""Class for ``ActionPartsMultiBullet`` action component."""
from dataclasses import dataclass
from math import floor

from dlparse.mono.asset.base import ActionComponentData
from .bullet import ActionBullet
from .bullet_arrange import ActionBulletArranged

__all__ = ("ActionBulletMulti",)


@dataclass
class ActionBulletMulti(ActionBullet):
    """
    Class of ``ActionPartsMultiBullet`` component in the player action asset.

    .. note::
        In enhanced Bellina S1 (``103505033``), collision interval (``_collisionHitInterval``)
        is not set to the "disabled sentinel" (sentinel = ``50``, actual = ``0.5``).

        Bullet duration (``_bulletDuration``) meaning unknown (value for enhanced Bellina S1 = ``0.4``.

        **``max_hit_count`` will still return ``0``**.
    """

    @classmethod
    def parse_raw(cls, data: ActionComponentData) -> "ActionBulletMulti":
        kwargs = cls.get_base_kwargs(data)

        bullet_count: int = data["_generateNum"]

        # Bullet may stay in the field for some time
        hit_count: int = max(floor(kwargs["bullet_duration"] / kwargs["collision_interval"]) + 1, 1)

        # Attach hit labels of the bullets
        labels_possible: list[str] = [data["_hitAttrLabel"]] * bullet_count * hit_count + data["_hitAttrLabelSubList"]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.extend(ActionBulletArranged.parse_raw(data["_arrangeBullet"]).hit_labels * bullet_count)

        # Attach collsion data
        kwargs.update({
            "collision_interval": data["_generateDelay"],
            # Kind of reversing the data structure to match the base signature
            "bullet_duration": bullet_count * data["_generateDelay"]
        })

        return ActionBulletMulti(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
