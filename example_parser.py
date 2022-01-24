from config_manager import config
from config_manager.config_types import BoolType, ListType


class TestConfig(config.Config):
    name: str
    age: int
    is_useful: BoolType = False
    parts: ListType[float]


my_config = TestConfig()
config.parse_env(my_config, prefix="test_config_")
config.parse_json(my_config, json_path="test_config.json")
config.parse_arguments(my_config, "TestConfig parser")

print(my_config)
