"""Implementations to check if the json schema matches the given body."""
from typing import Union

from dlparse.export.entry import JsonBody, JsonSchema
from .error import ArrayLengthInvalidError, KeyNotStringError, SchemaIsNotDictError, TypeNotAllowedError

__all__ = ("is_json_schema_match",)


# Monkey patch for the typing false negative
# - JSON schema comes from a class property (`@classmethod` with `@property`).
#   This causes the PyCharm type checker think it gets the property itself
#   instead of the property getter
def is_json_schema_match(schema: Union[JsonSchema, property], body: JsonBody):
    """
    Check if the json ``body`` matches ``schema``.

    Note that this only check for missing keys in ``schema``, but not ``body``.

    :class:`KeyNotStringError` will be raised if the schema key is not a string.

    :class:`ArrayMultipleValuesError` will be raised if an array defined in schema has multiple values.

    :class:`TypeNotAllowedError` will be raised if the schema type is not one of
    :class:`str`, :class:`int`, :class:`float`, :class:`bool`, :class:`list`, or :class:`dict`.

    :class:`SchemaIsNotDictError` will be raised if ``schema`` is not a :class:`dict`.
    """
    if not isinstance(schema, dict):
        raise SchemaIsNotDictError()

    return _check_schema(schema, body)


def _check_schema_list(schema_type: list[type], key: str, body: JsonBody):
    """Inner function to check if the body matches the schema type."""
    array_len = len(schema_type)
    # Check if the array length is not empty
    # - 1 for list of data
    # - 2+ for either one of the data type
    if not array_len:
        raise ArrayLengthInvalidError(key, array_len)

    # Check if the data type matches either one listed as `schema_type`
    if array_len > 1:
        return any(isinstance(body[key], type_) for type_ in schema_type)

    # Check if the corresponding content in the body is a list
    if not isinstance(body[key], list):
        return False

    # Check if all elements matches the desired type
    elem_type = schema_type[0]

    # `elem_type` is another schema
    if isinstance(elem_type, dict):
        return _check_schema(elem_type, body[key])

    # `elem_type` false positive - https://stackoverflow.com/a/56494823/11571888
    # noinspection PyTypeHints
    return all(isinstance(body_elem, elem_type) for body_elem in body[key])


# Flake 8 false-positive of "too complex"
def _check_schema(schema: JsonSchema, body: JsonBody):  # noqa: C901
    """
    Inner function to check if the json ``body`` matches ``schema``.

    :class:`KeyNotStringError` will be raised if the schema key is not a string.

    :class:`ArrayMultipleValuesError` will be raised if an array defined in schema has multiple values.

    :class:`TypeNotAllowedError` will be raised if the schema type is not one of
    :class:`str`, :class:`int`, :class:`float`, :class:`bool`, :class:`list`, or :class:`dict`.

    :class:`SchemaIsNotDictError` will be raised if ``schema`` is not a :class:`dict`.
    """
    if not isinstance(schema, type(body)) or schema.keys() != body.keys():
        return False

    for key, schema_type in schema.items():
        # Check if the key is a string
        if not isinstance(key, str):
            raise KeyNotStringError()

        # Check if the schema key is in the body
        if key not in body:
            return False

        # Check & handle if schema type is an array
        if isinstance(schema_type, list):
            if not _check_schema_list(schema_type, key, body):
                return False

            continue

        # Check & handle if the schema type is a map
        if isinstance(schema_type, dict):
            # Early return if the child schema does not match.
            # Otherwise, move forward.
            if not _check_schema(schema_type, body[key]):
                return False

            continue

        # Check if the schema type is valid
        if not issubclass(schema_type, (str, int, float, bool)):
            raise TypeNotAllowedError(key, schema_type)

        # Check if the value type in the body
        if not isinstance(body[key], schema_type):
            return False

    return True
