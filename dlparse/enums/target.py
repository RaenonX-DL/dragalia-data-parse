"""Hit target enum classes."""
from enum import Enum

from .mixin import TranslatableEnumMixin

__all__ = ("HitTarget", "HitTargetSimple")


class HitTargetSimple(TranslatableEnumMixin, Enum):
    """
    Target of an action in a simpler way.

    The difference between this and :class:`HitTarget` is that
    :class:`HitTarget` is the actual content in the game asset.
    The value of :class:`HitTarget` could be different even if the effective target is essentially the same,
    possibly due to some in-game mechanism.

    For example, ``HitTarget.SELF`` and ``HitTarget.HIT_DEPENDENT_SELF`` is effectively the same.
    The only difference is that ``HitTarget.HIT_DEPENDENT_SELF`` requires hit check; ``HitTarget.SELF`` does not.
    """

    UNKNOWN = -1

    SELF = 1
    SELF_SURROUNDING = 2
    ENEMY = 3
    FIELD = 4
    TEAM = 6

    @property
    def translation_id(self) -> str:
        return f"ENUM_TARGET_{self.name}"

    @staticmethod
    def get_all_translatable_members() -> list["HitTargetSimple"]:
        return [
            HitTargetSimple.SELF,
            HitTargetSimple.SELF_SURROUNDING,
            HitTargetSimple.ENEMY,
            HitTargetSimple.FIELD,
            HitTargetSimple.TEAM
        ]


class HitTarget(Enum):
    """
    Target of an action (hit attribute).

    This corresponds to the field ``_TargetGroup`` in the hit attribute asset.

    For the completed details, check
    ``https://github.com/dl-stuff/dl-datamine/blob/f6b6d604fd85b2ba69a0c01349c3b042972c9489/exporter/Mappings.py#L69``.
    """

    UNKNOWN = -1

    SELF = 1
    """The effect will be applied to the user themselves only."""
    SELF_SKILL_FIELD = 2
    """
    The effect will be applied to every ally who stays within the skill field range.

    This includes some skills that centers at the user (for example, Summer Cleo S2 ``106504012``),
    and the skills that creates a field (for example, Wedding Elisanne S1 ``101503021``).
    """
    ENEMY = 3
    """The effect will be applied to the enemy."""
    TEAM = 6
    """The effect will be applied to the whole team."""
    TEAM_LOWEST_HP = 7
    """The effect will be applied to the member who has the lowest HP% among the team, including the user."""
    HIT_OR_GUARDED_RECORD = 8
    # FIXME: (weilieh) Check the exact usage of this hit target
    """
    The effect applying condition is unknown.

    However, this appears for buff dispelling hits (along with hit exec type 6 - no damage).
    """
    HIT_DEPENDENT_SELF = 15
    """
    The effect will be applied to the user themselves, but it depends on how many times the skill hit.

    Note that skill hit does not mean the actual damaging hit.
    Instead, it just means that the skill "covers" the target.

    .. note::
        Used for Nadine S1 (``105501021``), Laranoa S2 (``106502012``) and Summer Cleo S2 (``106504012``).
    """

    def to_simple(self) -> HitTargetSimple:
        """Convert this hit target to the simplified version (:class:`HitTargetSimple`."""
        return TRANS_DICT_TO_SIMPLE[self]

    @classmethod
    def _missing_(cls, _):
        return HitTarget.UNKNOWN


TRANS_DICT_TO_SIMPLE: dict[HitTarget, HitTargetSimple] = {
    HitTarget.UNKNOWN: HitTargetSimple.UNKNOWN,
    HitTarget.SELF: HitTargetSimple.SELF,
    HitTarget.SELF_SKILL_FIELD: HitTargetSimple.SELF_SURROUNDING,
    HitTarget.ENEMY: HitTargetSimple.ENEMY,
    HitTarget.TEAM: HitTargetSimple.TEAM,
    HitTarget.HIT_OR_GUARDED_RECORD: HitTargetSimple.ENEMY,
    HitTarget.HIT_DEPENDENT_SELF: HitTargetSimple.SELF
}
"""A :class:`dict` to convert :class:`HitTarget` to the simplified version."""
