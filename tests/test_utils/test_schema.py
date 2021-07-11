import pytest

from tests.utils import is_json_schema_match
from tests.utils.error import (ArrayLengthInvalidError, KeyNotStringError, SchemaIsNotDictError, TypeNotAllowedError)


def test_match_simple():
    schema = {
        "num": int
    }
    body = {
        "num": 7
    }

    assert is_json_schema_match(schema, body)


def test_not_match_simple():
    schema = {
        "num": int
    }
    body = {
        "num": "string"
    }

    assert not is_json_schema_match(schema, body)


def test_match_simple_all_types():
    schema = {
        "num": int,
        "text": str,
        "decimal": float,
        "boolean": bool
    }
    body = {
        "num": 7,
        "text": "string",
        "decimal": 8.7,
        "boolean": True
    }

    assert is_json_schema_match(schema, body)


def test_one_of_not_match_simple_all_types():
    schema = {
        "num": int,
        "text": str,
        "decimal": float,
        "boolean": bool
    }
    body = {
        "num": 7,
        "text": 7,
        "decimal": 8.7,
        "boolean": True
    }

    assert not is_json_schema_match(schema, body)


def test_match_complex():
    schema = {
        "num": int,
        "array": [int],
        "map": {
            "inner": int
        }
    }
    body = {
        "num": 7,
        "array": [7, 8],
        "map": {
            "inner": 9
        }
    }

    assert is_json_schema_match(schema, body)


def test_not_match_in_list_complex():
    schema = {
        "num": int,
        "array": [int],
        "map": {
            "inner": int
        }
    }
    body = {
        "num": 7,
        "array": [7, "a"],
        "map": {
            "inner": 9
        }
    }

    assert not is_json_schema_match(schema, body)


def test_not_match_in_dict_complex():
    schema = {
        "num": int,
        "array": [int],
        "map": {
            "inner": int
        }
    }
    body = {
        "num": "not a num",
        "array": [7, 8],
        "map": {
            "inner": "a"
        }
    }

    assert not is_json_schema_match(schema, body)


def test_match_complex_all_types():
    schema = {
        "num": int,
        "text": str,
        "decimal": float,
        "boolean": bool,
        "map": {
            "inner": int,
            "something": str,
            "exponential": float,
            "flag": bool
        },
        "array": [str]
    }
    body = {
        "num": 7,
        "text": "a",
        "decimal": 8.7,
        "boolean": True,
        "map": {
            "inner": 9,
            "something": "b",
            "exponential": 3.33,
            "flag": False
        },
        "array": [
            "c",
            "d"
        ]
    }

    assert is_json_schema_match(schema, body)


def test_match_one_of_listed_type_first():
    schema = {
        "num": [int, str],
    }
    body = {
        "num": 7,
    }

    assert is_json_schema_match(schema, body)


def test_match_one_of_listed_type_second():
    schema = {
        "num": [int, str],
    }
    body = {
        "num": "7",
    }

    assert is_json_schema_match(schema, body)


def test_one_of_not_match_complex_all_types():
    schema = {
        "num": int,
        "text": str,
        "decimal": float,
        "boolean": bool,
        "map": {
            "inner": int,
            "something": str,
            "exponential": float,
            "flag": bool
        },
        "array": [str]
    }
    body = {
        "num": 7,
        "text": "a",
        "decimal": 8.7,
        "boolean": True,
        "map": {
            "inner": 9,
            "something": "b",
            "exponential": 3.33,
            "flag": 7
        },
        "array": [
            "c",
            "d"
        ]
    }

    assert not is_json_schema_match(schema, body)


def test_invalid_schema_key_not_string():
    schema = {
        7: int,
    }
    body = {
        7: 7,
    }

    with pytest.raises(KeyNotStringError):
        # noinspection PyTypeChecker
        is_json_schema_match(schema, body)


def test_invalid_schema_array_no_value():
    schema = {
        "num": [],
    }
    body = {
        "num": [7],
    }

    with pytest.raises(ArrayLengthInvalidError):
        is_json_schema_match(schema, body)


def test_invalid_schema_type_not_allowed():
    schema = {
        "num": object,
    }
    body = {
        "num": 7,
    }

    with pytest.raises(TypeNotAllowedError):
        is_json_schema_match(schema, body)


def test_invalid_schema_is_not_dict():
    schema = [7]
    body = {
        "num": 7,
    }

    with pytest.raises(SchemaIsNotDictError):
        # noinspection PyTypeChecker
        is_json_schema_match(schema, body)


def test_invalid_additional_key_in_body():
    schema = {
        "num": int
    }
    body = {
        "num": 7,
        "text": "s",
    }

    assert not is_json_schema_match(schema, body)


def test_invalid_additional_key_in_schema():
    schema = {
        "num": int,
        "text": str,
    }
    body = {
        "num": 7,
    }

    assert not is_json_schema_match(schema, body)
