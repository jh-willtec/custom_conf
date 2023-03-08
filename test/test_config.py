from unittest import TestCase

import custom_conf.errors as err
from custom_conf.properties.property import Property

from test.utils import TestConfig


class TestBaseConfig(TestCase):
    def test_add_after_init(self) -> None:
        c = TestConfig()
        with self.assertRaises(err.AddAfterInitError):
            c.this_fails = Property("this_fails", str)
