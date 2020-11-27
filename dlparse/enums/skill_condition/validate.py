"""Functions to validate the skill conditions."""
from typing import Optional, Iterable

from .category import SkillConditionCategories, SkillConditionCheckResult
from .items import SkillCondition


def validate_skill_conditions(conditions: Optional[Iterable[SkillCondition]] = None) -> SkillConditionCheckResult:
    """
    Check the validity of ``conditions``.

    If any of the following holds, conditions are considered invalid.

    - Multiple HP conditions exist.

    - Multiple buff counts exist.

    - Multiple bullet hit counts exist.

    - Multiple teammate coverages exist.

    - Multiple target elements exists.
    """
    # No conditions given
    if not conditions:
        return SkillConditionCheckResult.PASS

    # Categorical checks
    for category in SkillConditionCategories.get_all_categories():
        if not category.is_valid(conditions):
            return category.result_on_invalid

    return SkillConditionCheckResult.PASS
