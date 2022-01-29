"""This module provides configuration with built-in Python types."""

import os
from argparse import ArgumentParser
import json
from typing import Optional, Dict, Any

from config_manager.config_types import ListType


class Config:
    """
    Class to define required variables,
    their types and default values, for example:

    class BotConfig(Config):
        restart_on_failure: bool
        bot_name: str = "Example bot"

    """
    _parser_names = ["parse_env", "parse_arguments", "parse_json"]
    __annotations__: Dict[str, Any]

    def _is_variable_name(self, name: str) -> bool:
        return not name.startswith("_") and name not in self._parser_names

    def __repr__(self):
        return "\n".join(
            f"{v} = {getattr(self, v)}"
            for v in filter(self._is_variable_name, dir(self))
        )

    def parse_env(self, prefix: Optional[str] = None):
        """Parse config variables from Environment variables
        :param prefix: prefix for Environment variables; if None, no prefix is used
        """
        for variable_name, variable_type in self.__annotations__.items():
            expected_name = prefix + variable_name if prefix else variable_name
            if expected_name not in os.environ:
                continue

            variable_value = variable_type(os.environ.get(expected_name))
            setattr(self, variable_name, variable_value)

        return self

    def parse_arguments(self, parser_description: str):
        """Parse config variables from command line arguments
        :param parser_description: name of parser to show when used flag `-h` or `--help`
        """
        parser = ArgumentParser(parser_description)
        for variable_name, variable_type in self.__annotations__.items():
            if isinstance(variable_type, ListType):
                parser.add_argument(
                    f"--{variable_name}", nargs="*", type=variable_type.item_type
                )
            else:
                parser.add_argument(
                    f"--{variable_name}", type=variable_type, required=False
                )

        args, _ = parser.parse_known_args()
        for variable_name in self.__annotations__.keys():
            parsed_value = getattr(args, variable_name)
            if parsed_value is not None or not hasattr(self, variable_name):
                setattr(self, variable_name, parsed_value)

        return self

    def parse_json(self, json_path: str):
        """Parse config variables from json-config file
        :param json_path: path to json-config file
        """
        with open(json_path, encoding="utf-8") as config_file:
            json_variables = json.load(config_file)
            assert isinstance(json_variables, dict), "json config must be dictionary!"

        for variable_name, variable_type in self.__annotations__.items():
            if variable_name not in json_variables:
                continue

            setattr(
                self, variable_name, variable_type(json_variables.get(variable_name))
            )

        return self
