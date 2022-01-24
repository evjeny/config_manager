import os
import sys
from typing import List, Tuple, Union

from config_manager.config import Config
from config_manager.config_types import BoolType, ListType
from tests.base_test import BaseTest


class ListConfig(Config):
    int_array: ListType[int]
    str_array: ListType[str]
    float_array: ListType[float]
    bool_array: ListType[BoolType]


class TestListTypes(BaseTest):
    def setUp(self) -> None:
        self._config_targets: List[Tuple[Config, dict]] = [
            (
                ListConfig(),
                {
                    "int_array": [1, 2, 3],
                    "str_array": ["empty?", "", "1239"],
                    "float_array": [0.5, -999.23],
                    "bool_array": [True, False, True]
                }
            ),
            (
                ListConfig(),
                {
                    "int_array": [],
                    "str_array": [],
                    "float_array": [],
                    "bool_array": []
                }
            ),
        ]

    @staticmethod
    def _environment_variables_setuper(
        _: Config,
        target_values: dict,
        prefix: Union[None, str]
    ):
        for name, value in target_values.items():
            env_name = prefix + name if prefix else name
            if isinstance(value, list):
                env_value = ",".join(map(str, value))
            else:
                env_value = str(value)
            os.environ[env_name] = env_value
        print(os.environ)

    @staticmethod
    def _arguments_variables_setuper(_: Config, target_values: dict):
        sys.argv = sys.argv[:1]
        for variable, value in target_values.items():
            sys.argv.append(f"--{variable}")
            if isinstance(value, list):
                for item in value:
                    sys.argv.append(str(item))
            else:
                sys.argv.append(f"{value}")
        print(sys.argv)
