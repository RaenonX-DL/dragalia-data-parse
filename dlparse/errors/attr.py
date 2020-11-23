"""Attributal error classes."""

__all__ = ("ConfigError",)


class ConfigError(AttributeError):
    """Error to be raised if the class configuration is erroneous."""
