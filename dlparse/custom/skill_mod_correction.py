"""
Manual correction for the skill mods.

Assigned mods are applied to all of the skill hits.
"""

__all__ = ("mod_correction_rate",)

# K = Skill ID, V = Rate of Correction
# ------------------------------------
# Rate of Correction including the base.
# For example, to correct a skill mod from 2751% to 5502% (Summer Chelle S1 @ 2 Gauges, 107504043)
# The Rate of Correction is 2.
mod_correction_rate: dict[int, float] = {
    107504043: 2
}
