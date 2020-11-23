"""Mono behavior asset error classes."""
from abc import ABC

from dlparse.errors import AssetParsingError

__all__ = ("AssetKeyMissingError",)


class AssetKeyMissingError(AssetParsingError, ABC):
    """Error to be raised if the json key is missing."""

    def __init__(self, missing_key: str):
        super().__init__(f"Key `{missing_key}` not found in the asset data")
