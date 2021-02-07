"""Class for a single buffing hit."""
from dataclasses import dataclass

from dlparse.enums import ConditionComposite
from dlparse.mono.asset import ActionComponentBase
from .hit_conv import HitDataEffectConvertible

__all__ = ("BuffingHitData",)


@dataclass
class BuffingHitData(HitDataEffectConvertible[ActionComponentBase]):
    """Class for the data of a single buffing hit."""

    def get_hit_count(self, original_hit_count: int, condition_comp: ConditionComposite, ___) -> int:
        if self.is_effective_to_enemy(False):
            # Handle the case where the hit is effective to enemy
            if not self.hit_attr.damage_modifier:
                return 0  # Effective to enemy but does not deal damage (for example, dispel)

            # EXNOTE: Temporarily returns 1 for the effective hit attribute
            #   - Could be more if teammate coverage conditions available and
            #     the hit attribute is pivotal at the same time (not exist as of 2021/02/04)
            return 1 if self.hit_attr.is_effective_hit_count(original_hit_count) else 0

        return self.hit_attr.dummy_hit_count * ((condition_comp.teammate_coverage_converted or 0) + 1)
