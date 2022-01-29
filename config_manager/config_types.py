"""This module provides some implementations of config variables' types"""

from __future__ import annotations


class BoolType:  # pylint: disable=too-few-public-methods
    """Config type for boolean variables

    Will transform `str` variables with values
    "true", "yes", "1" and "on" to `True`, others to `False`.
    Will leave `bool` variables as they are.
    """

    def __new__(cls, value):
        _true_forms = {"true", "yes", "1", "on"}
        if isinstance(value, str):
            return value.lower() in _true_forms
        return bool(value)


class ListType(list):
    """Config type for lists with items of same type

    Can be used as `variable: ListType[str]`

    Will transform string by splitting it with commas, for example:
    `ListType[int]("1,2,3") == [1, 2, 3]`

    Will transform list by converting all its elements to type, for example:
    `ListType[int](["1", "2", "3"]) == [1, 2, 3]`
    """

    def __init__(self, item_type):
        super().__init__()
        self.item_type = item_type

    def __class_getitem__(cls, item_type):
        return cls(item_type)

    @staticmethod
    def empty_split(value: str, sep: str) -> list:
        """Splits string with separator

        If string is empty, then [] returned"""
        if value == "":
            return []
        return value.split(sep)

    def _cast_list(self, array: list):
        return [self.item_type(e) for e in array]

    def _cast_string(self, value: str):
        return self._cast_list(array=self.empty_split(value, sep=","))

    def __call__(self, value):
        if isinstance(value, str):
            return self._cast_string(value)
        if isinstance(value, list):
            return self._cast_list(value)

        raise Exception(f"Can't cast type {type(value)} to list of {self.item_type}")
