"""Util functions to process strings."""

__all__ = ("is_url",)


def is_url(string: str) -> bool:
    """Check if ``string`` is an URL."""
    return string.startswith("http")
