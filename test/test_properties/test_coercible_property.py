from unittest import TestCase

from custom_conf.properties.coercible_property import (
    IntProperty, FloatProperty,
    )

import custom_conf.errors as err

from test.utils import TestConfig


class CoercibleConfig(TestConfig):
    def _initialize_config_properties(self) -> None:
        self.int_prop = IntProperty("int_prop")
        self.float_prop = FloatProperty("float_prop")


class TestIntProperty(TestCase):
    def test_subclass_coercion(self) -> None:
        c = CoercibleConfig()
        c.int_prop = 1
        self.assertEqual(c.int_prop, 1)
        # False is 0, True is one
        c.int_prop = False
        self.assertEqual(c.int_prop, 0)
        c.int_prop = True
        self.assertEqual(c.int_prop, 1)

    def test_float_coercion(self) -> None:
        c = CoercibleConfig()
        c.int_prop = 1
        self.assertEqual(c.int_prop, 1)
        c.int_prop = float(1.0)
        self.assertEqual(c.int_prop, 1)

        invalid_values = [float("inf"), 4.2, float("nan")]
        for value in invalid_values:
            with (self.subTest(value),
                  self.assertRaises(err.InvalidCoercionError)
                  ):
                c.int_prop = value

    def test_str_coercion(self) -> None:
        c = CoercibleConfig()
        c.int_prop = 1
        self.assertEqual(c.int_prop, 1)
        c.int_prop = "1"
        self.assertEqual(c.int_prop, 1)
        c.int_prop = "1.0"
        self.assertEqual(c.int_prop, 1)
        with self.assertRaises(err.InvalidCoercionError) as e:
            c.int_prop = "1.337"
        with self.assertRaises(err.LossOfPrecisionError):
            raise e.exception.__cause__

        invalid_values = ["WA", "1.2", "1/3", ""]
        for value in invalid_values:
            with (self.subTest(value),
                  self.assertRaises(err.InvalidCoercionError)):
                c.int_prop = value

    def test_no_coercion(self) -> None:
        c = CoercibleConfig()
        c.int_prop = 0
        values = [CoercibleConfig, None, {1, 2}, {1: 2}, [1], (1,), b"1"]

        for value in values:
            with (self.subTest(value),
                  self.assertRaises(err.InvalidPropertyTypeError)):
                c.int_prop = value


class TestFloatProperty(TestCase):
    def test_subclass_coercion(self) -> None:
        # There are no implicit float types like False/True are for int.
        pass

    def test_int_coercion(self) -> None:
        c = CoercibleConfig()
        c.float_prop = 0.0
        self.assertEqual(c.float_prop, 0.0)
        c.float_prop = 1
        self.assertEqual(c.float_prop, 1.0)
        c.float_prop = 2
        self.assertEqual(c.float_prop, 2.0)
        # There are no invalid int values.

    def test_str_coercion(self) -> None:
        c = CoercibleConfig()
        c.float_prop = 0.0
        self.assertEqual(c.float_prop, 0.0)
        c.float_prop = "1.0"
        self.assertEqual(c.float_prop, 1.0)
        c.float_prop = "1.33"
        self.assertEqual(c.float_prop, 1.33)
        c.float_prop = "inf"
        self.assertEqual(c.float_prop, float("inf"))

        invalid_values = ["WA", " 1.1", "a1"]
        for value in invalid_values:
            with (self.subTest(value),
                  self.assertRaises(err.InvalidCoercionError)):
                c.int_prop = value

    def test_no_coercion(self) -> None:
        c = CoercibleConfig()
        c.float_prop = 0.0

        values = [CoercibleConfig, None, {1, 2}, {1: 2}, [1], (1,), b"1"]

        for value in values:
            with (self.subTest(value),
                  self.assertRaises(err.InvalidPropertyTypeError)):
                c.float_prop = value
