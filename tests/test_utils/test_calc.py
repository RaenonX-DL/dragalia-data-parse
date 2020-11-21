from dlparse.utils import multiply_matrix


def test_matrix_multiply_1():
    matrix = [[1, 3], [5, 7]]
    assert [[3, 9], [15, 21]] == multiply_matrix(matrix, 3)


def test_matrix_multiply_2():
    matrix = [[1, 4], [16, 20]]
    assert [[2.5, 10], [40, 50]] == multiply_matrix(matrix, 2.5)
