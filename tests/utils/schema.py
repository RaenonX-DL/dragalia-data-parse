"""Implementations to check if the json schema matches the given body."""
from typing import Type, Union

from .error import ArrayLengthInvalidError, KeyNotStringError, SchemaIsNotDictError, TypeNotAllowedError

__all__ = ("is_json_schema_match",)

Schema = dict[str, Type[Union[str, int, float, bool, list, 'Schema']]]
Body = dict[str, Union[str, int, float, bool, list, 'Body']]


def is_json_schema_match(schema: Schema, body: Body):
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


def _check_schema(schema: Schema, body: Body):
    """
    Inner function to check if the json ``body`` matches ``schema``.

    :class:`KeyNotStringError` will be raised if the schema key is not a string.

    :class:`ArrayMultipleValuesError` will be raised if an array defined in schema has multiple values.

    :class:`TypeNotAllowedError` will be raised if the schema type is not one of
    :class:`str`, :class:`int`, :class:`float`, :class:`bool`, :class:`list`, or :class:`dict`.

    :class:`SchemaIsNotDictError` will be raised if ``schema`` is not a :class:`dict`.
    """
    if type(schema) != type(body):
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
            array_len = len(schema_type)
            # Check if the array length is exactly 1
            if array_len != 1:
                raise ArrayLengthInvalidError(key, array_len)

            # Check if the corresponding content in the body is a list
            if not isinstance(body[key], list):
                return False

            # Check if all elements matches the desired type
            elem_type = schema_type[0]

            return all(isinstance(body_elem, elem_type) for body_elem in body[key])

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
