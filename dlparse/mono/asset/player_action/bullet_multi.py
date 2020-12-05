"""Class for ``ActionPartsMultiBullet`` action component."""
from dataclasses import dataclass
from typing import Union

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
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBulletMulti":
        kwargs = cls.get_base_kwargs(data)

        bullet_count: int = data["_generateNum"]

        # Attach hit labels of the bullets
        # This assumes ``_hitAttrLabel2nd`` is not duplicated by ``_generateNum``
        labels_possible: list[str] = [data["_hitAttrLabel"]] * bullet_count + [data["_hitAttrLabel2nd"]]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.extend(ActionBulletArranged.parse_raw(data["_arrangeBullet"]).hit_labels * bullet_count)

        # Attach collsion data
        kwargs |= {
            "collision_interval": data["_generateDelay"],
            # Kind of reversing the data structure to match the base signature
            "bullet_duration": bullet_count * data["_generateDelay"]
        }

        return ActionBulletMulti(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
