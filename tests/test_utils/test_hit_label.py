from dlparse.utils import get_hit_label_data, make_hit_label


def test_get_hit_label_no_level_no_shift():
    hit_label_data = get_hit_label_data("S071_000_00")

    assert hit_label_data.original == "S071_000_00"
    assert hit_label_data.level is None
    assert not hit_label_data.shifted


def test_get_hit_label_no_level_shifted():
    hit_label_data = get_hit_label_data("S071_000_00_HAS")

    assert hit_label_data.original == "S071_000_00"
    assert hit_label_data.level is None
    assert hit_label_data.shifted


def test_get_hit_label_has_level_no_shift():
    hit_label_data = get_hit_label_data("S072_001_00_LV01")

    assert hit_label_data.original == "S072_001_00"
    assert hit_label_data.level == 1
    assert not hit_label_data.shifted


def test_get_hit_label_has_level_shifted():
    hit_label_data = get_hit_label_data("S071_001_HAS_LV01")

    assert hit_label_data.original == "S071_001"
    assert hit_label_data.level == 1
    assert hit_label_data.shifted


def test_make_hit_label_no_level_no_shift():
    hit_label = make_hit_label("S071_000_00")

    assert hit_label == "S071_000_00"


def test_make_hit_label_no_level_shifted():
    hit_label = make_hit_label("S071_000_00", shifted=True)

    assert hit_label == "S071_000_00_HAS"


def test_make_hit_label_leveled_no_shift():
    hit_label = make_hit_label("S071_000_00", level=2)

    assert hit_label == "S071_000_00_LV02"


def test_make_hit_label_leveled_shifted():
    hit_label = make_hit_label("S071_000_00", level=1, shifted=True)

    assert hit_label == "S071_000_00_HAS_LV01"


def test_make_hit_label_using_leveled_shifted():
    hit_label = make_hit_label("S071_000_00_HAS_LV01", level=2, shifted=False)

    assert hit_label == "S071_000_00_LV02"


def test_make_hit_label_change_shift():
    hit_label = make_hit_label("S071_000_00_LV01", shifted=True)

    assert hit_label == "S071_000_00_HAS_LV01"


def test_make_hit_label_change_level_shifted():
    hit_label = make_hit_label("S071_000_00_HAS_LV01", level=2)

    assert hit_label == "S071_000_00_HAS_LV02"


def test_make_hit_label_change_level_no_shift():
    hit_label = make_hit_label("S071_000_00_LV01", level=2)

    assert hit_label == "S071_000_00_LV02"
