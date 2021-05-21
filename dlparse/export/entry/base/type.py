"""Type definitions for export entries."""
from typing import Any

__all__ = ("JsonSchema", "JsonBody")

# Recursive typing doesn't work

# JsonSchema = dict[str, Type[Union[str, int, float, bool, list, 'Schema']]]
JsonSchema = dict[str, Any]

# JsonBody = dict[str, Union[str, int, float, bool, list, 'Body']]
JsonBody = dict[str, Any]
