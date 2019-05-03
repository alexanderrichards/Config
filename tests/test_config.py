"""Tests for the config module."""
import unittest
import mock
from config._config2 import ConfigSystem, getConfig


class TestConfig(unittest.TestCase):
    """Unit tests for ConfigSystem."""

    def test_setup(self):
        ConfigSystem.get_instance()


if __name__ == '__main__':
    unittest.main()
