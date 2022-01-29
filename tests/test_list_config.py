"""Test list types provided by config_manager"""

from typing import List, Tuple, Any

from config_manager.config import Config
from config_manager.config_types import BoolType, ListType

from tests.base_test import BaseTest


class ListConfig(Config):  # pylint: disable=too-few-public-methods
    """Config with some list types with different item types"""

    int_array: ListType[int]
    str_array: ListType[str]
    float_array: ListType[float]
    bool_array: ListType[BoolType]


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
            env_value = ",".join(map(str, value))
        else:
            env_value = str(value)

        environ[name] = env_value

    @staticmethod
    def _append_to_argv(argv: list, name: str, value: Any):
        argv.append(f"--{name}")
        if isinstance(value, list):
            for item in value:
                argv.append(str(item))
        else:
            argv.append(f"{value}")
