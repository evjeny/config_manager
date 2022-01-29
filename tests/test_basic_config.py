"""Test built-in types provided by config_manager"""

from typing import List, Tuple

from config_manager.config import Config
from config_manager.config_types import BoolType
from tests.base_test import BaseTest


class BasicConfig(Config):
    """Config with some variables of built-in types"""

    name: str
    age: int
    happiness: float
    is_cool: BoolType


class TestBasicTypes(BaseTest):
    """Test case for built-in type parsers"""

    def setUp(self) -> None:
        self._config_targets: List[Tuple[Config, dict]] = [
            (
                BasicConfig(),
                {"name": "evjeny", "age": 1000, "happiness": 0.5, "is_cool": True},
            ),
            (
                BasicConfig(),
                {
                    "name": "Papanya",
                    "age": 1_000_000,
                    "happiness": 999.99,
                    "is_cool": True,
                },
            ),
            (
                BasicConfig(),
                {"name": "Techies", "age": -13, "happiness": -5.4, "is_cool": False},
            ),
        ]
