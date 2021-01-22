from dlparse.utils import remove_duplicates_preserve_order


def test_remove_dup_list():
    assert remove_duplicates_preserve_order([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert remove_duplicates_preserve_order([1, 2, 2, 3, 4]) == [1, 2, 3, 4]
    assert remove_duplicates_preserve_order([1, 1, 1, 1, 1]) == [1]


def test_remove_dup_tuple():
    assert remove_duplicates_preserve_order((1, 2, 3, 4)) == (1, 2, 3, 4)
    assert remove_duplicates_preserve_order((1, 2, 2, 3, 4)) == (1, 2, 3, 4)
    assert remove_duplicates_preserve_order((1, 1, 1, 1, 1)) == (1,)
