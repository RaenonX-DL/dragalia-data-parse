"""Errors for json schema checking function."""
__all__ = ("KeyNotStringError", "ArrayLengthInvalidError", "TypeNotAllowedError", "SchemaIsNotDictError")


class KeyNotStringError(ValueError):
    """Error to be raised if any of the schema key is not a string."""

    def __init__(self):
        super().__init__("All keys of the schema must be a string.")


class ArrayLengthInvalidError(ValueError):
    """Error to be raised if the array definition in schema is invalid."""

    def __init__(self, key: str, array_len: int):
        super().__init__(f"Array definition of key `{key}` must be exactly of length 1 (current: {array_len}).")


class TypeNotAllowedError(TypeError):
    """Error to be raised if the schema contains any unallowed type."""

    def __init__(self, key: str, key_type: type):
        super().__init__(
            f"Type for {key} ({key_type}) is not allowed. "
            f"The only allowed types are {bool}, {int}, {float}, and {str}."
        )


class SchemaIsNotDictError(TypeError):
    """Error to be raised if schema is not a dict."""

    def __init__(self):
        super().__init__("JSON schema must be a dict.")
