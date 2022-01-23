from config_manager import config


class TestConfig(config.Config):
    name: str
    age: int
    is_useful: bool = False


my_config = TestConfig()
config.parse_env(my_config, prefix="test_config_")
config.parse_json(my_config, json_path="test_config.json")
config.parse_arguments(my_config, "TestConfig parser")

print(my_config)
