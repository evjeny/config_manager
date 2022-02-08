"""Test list types provided by config_manager"""

from typing import List, Tuple, Any

from config_manager.config import Config
from config_manager.variable_parsers import ListType

from tests.base_test import BaseTest


class ListConfig(Config):
    """Config with some list types with different item types"""

    int_array: ListType[int]
    str_array: ListType[str]
    float_array: ListType[float]
    bool_array: ListType[bool]


def _list_to_str(data: list) -> str:
    return "[" + ",".join(map(str, data)) + "]"


class TestListTypes(BaseTest):
    """Test case for list parsers"""

    def setUp(self) -> None:
        self._config_targets: List[Tuple[Config, dict]] = [
            (
                ListConfig(),
                {
                    "int_array": [1, 2, 3],
                    "str_array": ["empty?", "", "1239"],
                    "float_array": [0.5, -999.23],
                    "bool_array": [True, False, True],
                },
            ),
            (
                ListConfig(),
                {"int_array": [], "str_array": [], "float_array": [], "bool_array": []},
            ),
        ]

    @staticmethod
    def _append_to_env(environ, name: str, value):
        if isinstance(value, list):
            env_value = _list_to_str(value)
        else:
            env_value = str(value)

        environ[name] = env_value

    @staticmethod
    def _append_to_argv(argv: list, name: str, value: Any):
        argv.append(f"--{name}")
        if isinstance(value, list):
            argv.append(_list_to_str(value))
        else:
            argv.append(f"{value}")
