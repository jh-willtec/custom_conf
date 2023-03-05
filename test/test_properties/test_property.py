from unittest import TestCase

from custom_conf.properties.property import Property
import custom_conf.errors as err

from test.utils import TestConfig


class PropertyConfig(TestConfig):
    def _initialize_config_properties(self) -> None:
        self.str_prop = Property("str_prop", str)
        self.int_prop = Property("int_prop", int)
        super()._initialize_config_properties()


class TestProperty(TestCase):
    def test_property(self) -> None:
        c = PropertyConfig()
        with self.assertRaises(err.MissingRequiredPropertyError):
            _ = c.str_prop
        c.str_prop = ""
        self.assertEqual("", c.str_prop)
        c.str_prop = "test"
        self.assertEqual("test", c.str_prop)
        invalid_values = [["t", "e", "s", "t"], 1, 0, -1]
        for i, invalid_value in enumerate(invalid_values):
            with (self.subTest(i=i),
                  self.assertRaises(err.InvalidPropertyTypeError)):
                c.str_prop = invalid_value

    def test_int_property(self) -> None:
        c = PropertyConfig()
        with self.assertRaises(err.MissingRequiredPropertyError):
            _ = c.int_prop
        c.int_prop = 0
        self.assertEqual(0, c.int_prop)
        c.int_prop += 1
        self.assertEqual(1, c.int_prop)
        invalid_values = [0.1, "0", "0.0", 0., -1.0, [0], {0: 0}]
        for i, invalid_value in enumerate(invalid_values):
            with (self.subTest(i=i),
                  self.assertRaises(err.InvalidPropertyTypeError)):
                c.int_prop = invalid_value
