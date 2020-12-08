"""Functions for mimicking the in-game computations."""
__all__ = ("calculate_crisis_mod",)


def calculate_crisis_mod(mod: float, hp_rate: float, crisis_rate: float) -> float:
    """
    Calculate the ``mod``, which correlates to ``crisis_rate``, at ``hp_rate``.

    In short, this is quadratic.
    """
    return mod * ((1 - hp_rate) ** 2 * (crisis_rate - 1) + 1)
