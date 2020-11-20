"""Models for character skills."""
from dataclasses import dataclass, field

from dlparse.mono.asset import HitAttrEntry

__all__ = ("AttackingSkillData",)


@dataclass
class AttackingSkillData:
    """
    An attacking skill data.

    Both ``hit_count`` and ``mods`` should be sorted by the skill level.

    For example, if skill level 1 has 1 hit and 100% mods while skill level 2 has 2 hits and 150% + 200% mods,
    ``hit_count`` should be ``[1, 2]`` and ``mods`` should be ``[[1.0], [1.5, 2.0]]``.
    """

    hit_count: list[int]
    mods: list[list[float]]

    damage_hit_attrs: list[list[HitAttrEntry]]

    total_mod: list[float] = field(init=False)

    def __post_init__(self):
        self.total_mod = [sum(mods) for mods in self.mods]

    @property
    def hit_count_at_max(self) -> int:
        """Get the skill hit count at the max level."""
        return self.hit_count[-1]

    @property
    def total_mod_at_max(self) -> float:
        """Get the total skill modifier at the max level."""
        return self.total_mod[-1]

    @property
    def mods_at_max(self) -> list[float]:
        """Get the skill modifiers at the max level."""
        return self.mods[-1]

    @property
    def max_available_level(self) -> int:
        """
        Get the max available level of a skill.

        This max level does **NOT** reflect the actual max level in-game.
        To get such, character data is needed.
        """
        return len(self.hit_count)
