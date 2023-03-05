from unittest import TestCase

from custom_conf.properties.nested_property import (
    IntListProperty, NestedTypeProperty)
import custom_conf.errors as err
from test.utils import TestConfig


class NestedConfig(TestConfig):
    def _initialize_config_properties(self) -> None:
        self.list_prop1 = NestedTypeProperty("n1", list[int])
        # No need to explicitely test IntListProperty,
        # as it is only a shorthand for the above.
        self.list_prop2 = IntListProperty("list1")
        self.dict_prop = NestedTypeProperty("n2", dict[str: int])
        super()._initialize_config_properties()


class TestNestedTypeProperty(TestCase):
    def test_nested_type_property_list(self) -> None:
        c = NestedConfig()
        c.list_prop1 = []
        self.assertEqual([], c.list_prop1)
        # We can not prevent this.
        c.list_prop1.append("1")
        self.assertEqual(["1"], c.list_prop1)
        # But adding like this will fail
        c.list_prop1 = []
        with self.assertRaises(err.InvalidPropertyTypeError):
            c.list_prop1 += ["3"]
        # This will fail for the same reason.
        c.list_prop1 = []
        c.list_prop1.append("1")
        with self.assertRaises(err.InvalidPropertyTypeError):
            c.list_prop1 += [3]
        q = [1, 2, 3]
        c.list_prop1 = q
        self.assertEqual(q, c.list_prop1)
        c.list_prop2 = q
        self.assertEqual(q, c.list_prop2)
        # No copies are created.
        self.assertEqual(id(q), id(c.list_prop1))
        self.assertEqual(id(q), id(c.list_prop2))
        c.list_prop1.append(4)
        self.assertEqual([1, 2, 3, 4], q)

    def test_nested_type_property_dict(self) -> None:
        c = NestedConfig()
        c.dict_prop = {}
        self.assertEqual({}, c.dict_prop)
        c.dict_prop["test"] = 42
        self.assertDictEqual({"test": 42}, c.dict_prop)
        # We can not prevent this.
        c.dict_prop[42] = "test"
        self.assertDictEqual({"test": 42, 42: "test"}, c.dict_prop)
