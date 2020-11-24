"""Functions for easier calculations."""
__all__ = ("multiply_vector", "multiply_matrix",)


def multiply_vector(vector: list[float], multiplier: float) -> list[float]:
    """Multiply ``vector`` by ``multiplier``. This does not modify ``vector`` itself."""
    return [item * multiplier for item in vector]


def multiply_matrix(matrix: list[list[float]], multiplier: float) -> list[list[float]]:
    """Multiply all the entries in the ``matrix`` by ``multiplier``. This does not modify ``matrix`` itself."""
    return [multiply_vector(vector, multiplier) for vector in matrix]
