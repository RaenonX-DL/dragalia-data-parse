"""Attributal error classes."""

__all__ = ("ConfigError",)


class ConfigError(AttributeError):
    """Error to be raised if the class configuration is erroneous."""

    def __init__(self, message: str):
        super().__init__(message)
