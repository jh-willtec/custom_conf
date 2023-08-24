from __future__ import annotations

import abc
from typing import Any, Optional, Type

import custom_conf.errors as err
from custom_conf.properties.coercible_property import (
    FloatProperty, IntProperty,
    )
from custom_conf.properties.property import Property


class BoundedProperty(Property, abc.ABC):
    """ Used for properties with bounded values (closed interval). """

    def __init__(
            self, name: str, attr_type: type, lower=None, upper=None) -> None:
        # Subclasses must call self._initialize_bounds.
        super().__init__(name, attr_type)
        self.lower = lower
        self.upper = upper

    @property
    def lower(self) -> Any:
        if not self._lower:
            return None
        # noinspection PyTypeChecker
        return self._lower.__get__(self)

    @lower.setter
    def lower(self, value: Any):
        if value is None:
            self._lower = None
            return
        self._lower.__set__(self, value)

    @property
    def upper(self) -> Any:
        if not self._upper:
            return None
        # noinspection PyTypeChecker
        return self._upper.__get__(self)

    @upper.setter
    def upper(self, value: Any):
        if value is None:
            self._upper = None
            return
        self._upper.__set__(self, value)

    def _initialize_bounds(
            self, prop: Optional[Type[Property]], *args) -> None:
        self._lower = prop("_lower", *args) if prop else prop
        self._upper = prop("_upper", *args) if prop else prop
        self._value = prop("_value", *args) if prop else prop

    def _validate_within_bounds(self, value: Any):
        """ Check if the given value is between the bounds. """
        upper_oob = self.upper is not None and value > self.upper
        lower_oob = self.lower is not None and value < self.lower
        if upper_oob or lower_oob:
            raise err.OutOfBoundsPropertyError(prop=self, value=value)

    def validate(self, value: Any) -> None:
        """ Checks if the value is within bounds. """
        super().validate(value)
        self._validate_within_bounds(value)

    def __set__(self, obj, value: Any):
        try:
            self._value.__set__(self, value)
            # noinspection PyTypeChecker
            value = self._value.__get__(self)
        except err.PropertyError:
            raise err.InvalidPropertyTypeError(prop=self, type=type(value))
        super().__set__(obj, value)


class FloatBoundedProperty(BoundedProperty):
    """ Bounded property of type float. """

    def __init__(self, name, lower: float = None, upper: float = None) -> None:
        self._initialize_bounds(FloatProperty)
        super().__init__(name, float, lower, upper)


class IntBoundedProperty(BoundedProperty):
    """ Bounded property of type int. """

    def __init__(self, name, lower: int = None, upper: int = None) -> None:
        self._initialize_bounds(IntProperty)
        super().__init__(name, int, lower, upper)
