import pytest

from dlparse.utils import multiply_matrix, calculate_crisis_mod


def test_matrix_multiply_1():
    matrix = [[1, 3], [5, 7]]
    assert [[3, 9], [15, 21]] == multiply_matrix(matrix, 3)


def test_matrix_multiply_2():
    matrix = [[1, 4], [16, 20]]
    assert [[2.5, 10], [40, 50]] == multiply_matrix(matrix, 2.5)


crisis_mod_gt_1_data = [
    [1000, 1, 2, 1000],
    [1000, 0.7, 2, 1090],
    [1000, 0.5, 2, 1250],
    [1000, 0.3, 2, 1490],
    [1000, 0.2, 2, 1640],
    [1000, 0.1, 2, 1810],
]


@pytest.mark.parametrize(["original_mod", "current_hp", "crisis_mod", "expected_result"], crisis_mod_gt_1_data)
def test_crisis_mod_gt_1(original_mod: float, current_hp: float, crisis_mod: float, expected_result: float):
    assert calculate_crisis_mod(original_mod, current_hp, crisis_mod) == pytest.approx(expected_result)


crisis_mod_lt_1_data = [
    [1000, 1, 0.5, 1000],
    [1000, 0.7, 0.5, 955],
    [1000, 0.5, 0.5, 875],
    [1000, 0.3, 0.5, 755],
    [1000, 0.2, 0.5, 680],
    [1000, 0.1, 0.5, 595],
]


@pytest.mark.parametrize(["original_mod", "current_hp", "crisis_mod", "expected_result"], crisis_mod_gt_1_data)
def test_crisis_mod_lt_1(original_mod: float, current_hp: float, crisis_mod: float, expected_result: float):
    assert calculate_crisis_mod(original_mod, current_hp, crisis_mod) == pytest.approx(expected_result)
