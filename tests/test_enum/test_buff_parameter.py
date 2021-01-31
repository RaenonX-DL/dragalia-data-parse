from dlparse.enums import BuffParameter, get_image_path


def test_has_unit():
    for buff_param in BuffParameter:
        _ = buff_param.parameter_unit


def test_has_image():
    for buff_param in BuffParameter:
        get_image_path(buff_param)
