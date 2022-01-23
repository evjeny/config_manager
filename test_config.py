from argparse import ArgumentParser
import json
import os
import sys

from config_manager.config import Config, parse_env, parse_arguments, parse_json


class TestConfig(Config):
    name: str
    age: int
    happiness: float
    is_cool: bool


target_values = {
        "name": "Mister Smith",
        "age": 24,
        "happiness": 0.5,
        "is_cool": True
    }


def _check_parsed_arguments(config: Config):
    for name, value in target_values.items():
        assert getattr(config, name) == value, "config variable wasn't assigned correctly"


def test_environment():
    for prefix in [None, "super_long_prefix_omagad_", "test_"]:
        for name, value in target_values.items():
            env_name = prefix + name if prefix else name
            env_value = str(value)
            os.environ[env_name] = env_value

        config = TestConfig()
        parse_env(config, prefix)

    _check_parsed_arguments(config)
    print("Environment test passed")


def test_arguments():
    sys.argv = sys.argv[:1]
    for variable, value in target_values.items():
        sys.argv.append(f"--{variable}")
        sys.argv.append(f"{value}")

    config = TestConfig()
    parse_arguments(config, "Super ArgumentParser v1.0")

    _check_parsed_arguments(config)
    print("Arguments test passed")


def test_json(temp_filename: str = "_hidden_config.json"):
    with open(temp_filename, "w+") as f:
        json.dump(target_values, f)

    config = TestConfig()
    parse_json(config, temp_filename)
    os.remove(temp_filename)

    _check_parsed_arguments(config)
    print("JSON test passed")


if __name__ == "__main__":
    parser = ArgumentParser("Test ConfigManager")
    parser.add_argument("--test_env", action="store_true", help="test parsing of environment variables")
    parser.add_argument("--test_arguments", action="store_true", help="test parsing of script arguments")
    parser.add_argument("--test_json", action="store_true", help="test parsing of json config")
    parser.add_argument("--all", action="store_true", help="run all tests")
    args = parser.parse_args()

    if args.all:
        test_environment()
        test_arguments()
        test_json()
    else:
        if args.test_env:
            test_environment()
        if args.test_arguments:
            test_arguments()
        if args.test_json:
            test_json()
