from unittest import TestCase

import custom_conf.errors as err
from custom_conf.properties.bounded_property import (
    BoundedProperty, FloatBoundedProperty, IntBoundedProperty)

from test.utils import TestConfig


class BoundedConfig(TestConfig):
    def _initialize_config_properties(self) -> None:
        self.bp1 = BoundedProperty("bp1", str, "b", "y")
        self.fbp = FloatBoundedProperty("fbp", -1.0, 30.)
        self.ibp = IntBoundedProperty("ibp", upper=30)
        super()._initialize_config_properties()


class TestBoundedProperty(TestCase):
    def test_bounded_property(self) -> None:
        c = BoundedConfig()
        invalid_values = [("a", err.OutOfBoundsPropertyError),
                          ("z", err.OutOfBoundsPropertyError),
                          (3, err.InvalidPropertyTypeError)]
        for i, (value, error) in enumerate(invalid_values[:1]):
            with (self.subTest(i=i), self.assertRaises(error)):
                c.bp1 = value

        inval = [(str, "", "", err.InvalidBoundOrderError),
                 (str, 1, "", err.InvalidLowerBoundsError),
                 (str, "", 1, err.InvalidUpperBoundsError),
                 (1, 1, 2, err.NotATypeError),
                 ]
        for i, (typ, lower, upper, error) in enumerate(inval):
            with self.assertRaises(error):
                BoundedProperty("bp", typ, lower, upper)


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
        # Convertible types still don't work.
        with self.assertRaises(err.InvalidPropertyTypeError):
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
        # Convertible types still don't work.
        with self.assertRaises(err.InvalidPropertyTypeError):
            c.ibp = float(3)
        # Out of bounds.
        with self.assertRaises(err.OutOfBoundsPropertyError):
            c.ibp = 33
        # Bounds use an open interval.
        c.ibp = 30
        self.assertEqual(30, c.ibp)
