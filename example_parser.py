"""Example usage of config_manager module"""

from config_manager.config import Config
from config_manager.config_types import BoolType, ListType


class TestConfig(Config):
    """Config example with some variables of different types"""

    name: str
    age: int
    is_useful: BoolType = False
    parts: ListType[float]


my_config = TestConfig() \
    .parse_env(prefix="test_config_") \
    .parse_json(json_path="test_config.json") \
    .parse_arguments("TestConfig parser")

print(my_config)
