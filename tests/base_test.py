import json
import os
import sys
from functools import partial
from typing import List, Tuple, Union, Callable
import unittest

from config_manager.config import Config
from config_manager.config import parse_env, parse_arguments, parse_json


class BaseTest(unittest.TestCase):
    _config_targets: List[Tuple[Config, dict]] = []

    @staticmethod
    def get_json_filename() -> str:
        return "_json_config.json"

    def _check_parsed_arguments(self, config: Config, target_values: dict):
        for name, value in target_values.items():
            self.assertEqual(
                getattr(config, name),
                value,
                "config variable must be assigned correctly"
            )

    def _check_multiple_targets(
            self,
            variables_setuper: Callable[[Config, dict], None],
            parser: Callable[[Config], None]
    ):
        for i, (config_object, target_values) in enumerate(
            self._config_targets
        ):
            with self.subTest(i=i):
                variables_setuper(config_object, target_values)
                parser(config_object)
                self._check_parsed_arguments(config_object, target_values)

    @staticmethod
    def _predefined_variables_setuper(config: Config, target_values: dict):
        for variable_name, variable_value in target_values.items():
            setattr(config, variable_name, variable_value)

    @staticmethod
    def _predefined_parser(_: Config):
        pass

    def test_predefined(self):
        self._check_multiple_targets(
            self._predefined_variables_setuper,
            self._predefined_parser
        )

    @staticmethod
    def _environment_variables_setuper(
        _: Config,
        target_values: dict,
        prefix: Union[None, str]
    ):
        for name, value in target_values.items():
            env_name = prefix + name if prefix else name
            env_value = str(value)
            os.environ[env_name] = env_value

    def test_environment(self):
        for p in [None, "usual_prefix_", "_999_"]:
            self._check_multiple_targets(
                partial(self._environment_variables_setuper, prefix=p),
                partial(parse_env, prefix=p)
            )

    @staticmethod
    def _arguments_variables_setuper(_: Config, target_values: dict):
        sys.argv = sys.argv[:1]
        for variable, value in target_values.items():
            sys.argv.append(f"--{variable}")
            sys.argv.append(f"{value}")
        print(sys.argv)

    def test_arguments(self):
        self._check_multiple_targets(
            self._arguments_variables_setuper,
            partial(parse_arguments, parser_description="Test parser")
        )

    @staticmethod
    def _json_variables_setuper(_: Config, target_values: dict, filename: str):
        with open(filename, "w+") as f:
            json.dump(target_values, f)

    def test_json(self):
        self._check_multiple_targets(
            partial(
                self._json_variables_setuper,
                filename=self.get_json_filename()
            ),
            partial(parse_json, json_path=self.get_json_filename())
        )

        if os.path.exists(self.get_json_filename()):
            os.remove(self.get_json_filename())
