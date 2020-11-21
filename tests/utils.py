import pytest


def approx_matrix(data: list[list[float]]):
    """``pytest.approx()`` for a matrix."""
    return [pytest.approx(subdata) for subdata in data]
