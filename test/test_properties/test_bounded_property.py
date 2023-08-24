from unittest import TestCase

import custom_conf.errors as err
from custom_conf.properties.bounded_property import (
    BoundedProperty, FloatBoundedProperty, IntBoundedProperty)

from test.utils import TestConfig


class BoundedConfig(TestConfig):
    def _initialize_config_properties(self) -> None:
        self.fbp = FloatBoundedProperty("fbp", -1.0, 30.)
        self.ibp = IntBoundedProperty("ibp", upper=30)
        super()._initialize_config_properties()


class TestFloatBoundedPropert(TestCase):
    def test_float_bounded_property(self) -> None:
        c = BoundedConfig()
        fbp = object.__getattribute__(c, "fbp")
        # Correct bounds.
        self.assertEqual(-1., fbp.lower)
        self.assertEqual(30., fbp.upper)
        # Invalid type.
        with self.assertRaises(err.InvalidPropertyTypeError):
            c.fbp = "a"
        # Coercible types work.
        c.fbp = int(3)
        # Out of bounds.
        with self.assertRaises(err.OutOfBoundsPropertyError):
            c.fbp = -1.1
        with self.assertRaises(err.OutOfBoundsPropertyError):
            c.fbp = 33.
        # Bounds use an open interval.
        c.fbp = -1.
        self.assertEqual(-1., c.fbp)
        c.fbp = 30.
        self.assertEqual(30., c.fbp)


class TestIntFloatBoundedProperty(TestCase):
    def test_int_bounded_property(self) -> None:
        c = BoundedConfig()
        ibp = object.__getattribute__(c, "ibp")
        # Correct bounds.
        self.assertEqual(None, ibp.lower)
        self.assertEqual(30., ibp.upper)
        # Invalid type.
        with self.assertRaises(err.InvalidPropertyTypeError):
            c.ibp = "a"
        # Coercible types work.
        c.ibp = float(3)
        # Out of bounds.
        with self.assertRaises(err.OutOfBoundsPropertyError):
            c.ibp = 33
        # Bounds use an open interval.
        c.ibp = 30
        self.assertEqual(30, c.ibp)
