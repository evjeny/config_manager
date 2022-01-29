"""Base testing entity for all parsers"""

import json
import os
import sys
import unittest
from functools import partial
from typing import List, Tuple, Union, Callable, Any

from config_manager.config import Config


class BaseTest(unittest.TestCase):
    """Superclass for test entities"""

    _config_targets: List[Tuple[Config, dict]] = []
    _json_filename: str = "_json_config.json"

    def _check_parsed_arguments(self, config: Config, target_values: dict):
        for name, value in target_values.items():
            self.assertEqual(
                getattr(config, name),
                value,
                "config variable must be assigned correctly",
            )

    def _check_multiple_targets(
        self,
        variables_setuper: Callable[[Config, dict], None],
        parser: Callable[[Config], None],
    ):
        for i, (config_object, target_values) in enumerate(self._config_targets):
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
        """Test predefined parser"""
        self._check_multiple_targets(
            self._predefined_variables_setuper, self._predefined_parser
        )

    @staticmethod
    def _append_to_env(environ, name: str, value):
        environ[name] = str(value)

    def _environment_variables_setuper(
        self, _: Config, target_values: dict, prefix: Union[None, str]
    ):
        for name, value in target_values.items():
            env_name = prefix + name if prefix else name
            self._append_to_env(os.environ, env_name, value)

    def test_environment(self):
        """Test environment parser"""

        def parse_env(config: Config, prefix: Union[None, str]):
            config.parse_env(prefix=prefix)

        for env_prefix in [None, "usual_prefix_", "_999_"]:
            self._check_multiple_targets(
                partial(self._environment_variables_setuper, prefix=env_prefix),
                partial(parse_env, prefix=env_prefix),
            )

    @staticmethod
    def _append_to_argv(argv: list, name: str, value: Any):
        argv.append(f"--{name}")
        argv.append(str(value))

    def _arguments_variables_setuper(self, _: Config, target_values: dict):
        sys.argv = sys.argv[:1]
        for variable, value in target_values.items():
            self._append_to_argv(sys.argv, variable, value)

    def test_arguments(self):
        """Test argument parser"""

        def parse_arguments(config: Config, parser_description: str):
            config.parse_arguments(parser_description)

        self._check_multiple_targets(
            self._arguments_variables_setuper,
            partial(parse_arguments, parser_description="Test parser"),
        )

    @staticmethod
    def _json_variables_setuper(_: Config, target_values: dict, filename: str):
        with open(filename, "w+", encoding="utf-8") as config_file:
            json.dump(target_values, config_file)

    def test_json(self):
        """Test json parser"""

        def parse_json(config: Config, json_path: str):
            config.parse_json(json_path)

        self._check_multiple_targets(
            partial(self._json_variables_setuper, filename=self._json_filename),
            partial(parse_json, json_path=self._json_filename),
        )

        if os.path.exists(self._json_filename):
            os.remove(self._json_filename)
