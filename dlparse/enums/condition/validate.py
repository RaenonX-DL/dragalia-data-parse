"""Functions to validate the conditions."""
from typing import Iterable, Optional

from .category import ConditionCategories, ConditionCheckResult
from .items import Condition


def validate_conditions(conditions: Optional[Iterable[Condition]] = None) -> ConditionCheckResult:
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
        return ConditionCheckResult.PASS

    # Categorical checks
    for category in ConditionCategories.get_all_categories():
        if not category.is_valid(conditions):
            return category.result_on_invalid

    return ConditionCheckResult.PASS
