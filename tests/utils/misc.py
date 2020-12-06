"""Miscellaneous helper implementations."""
import pytest

__all__ = ("approx_matrix",)


def approx_matrix(data: list[list[float]]):
    """``pytest.approx()`` for a matrix."""
    return [pytest.approx(subdata) for subdata in data]
