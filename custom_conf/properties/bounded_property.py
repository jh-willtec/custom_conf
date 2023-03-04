from __future__ import annotations

from typing import Any

import errors as err
from properties.property import Property


class BoundedProperty(Property):
    """ Used for properties with bounded values (closed interval). """

    def __init__(
            self, name: str, attr_type: type, lower=None, upper=None) -> None:
        super().__init__(name, attr_type)
        self.lower = lower
        self.upper = upper
        self._validate_init_values()

    def _validate_init_values(self) -> None:
        """ Check if the given bounds and type are valid bound values. """
        # Check at least one of lower/upper is given.
        lower_exists = self.lower is not None
        upper_exists = self.upper is not None
        if not lower_exists and not upper_exists:
            raise err.MissingBoundsError
        # Check if the type is comparable.
        try:
            # noinspection PyStatementEffect
            lower_exists and self.lower < self.lower
            # noinspection PyStatementEffect
            upper_exists and self.upper < self.upper
        except TypeError:
            raise err.IncomparableBoundsTypeError(self.type)
        # Bounds need to be of the same type as the excepted property type.
        if self.lower is not None and not isinstance(self.type, self.lower):
            raise err.InvalidLowerBoundsError(self.type, self.lower)
        if self.upper is not None and not isinstance(self.type, self.upper):
            raise err.InvalidUpperBoundsError(self.type, self.lower)

    def _validate_within_bounds(self, value: Any):
        """ Check if the given value is between the bounds. """
        upper_oob = self.upper is not None and value > self.upper
        lower_oob = self.lower is not None and value < self.lower
        if upper_oob or lower_oob:
            raise err.OutOfBoundsPropertyError(self, value)

    def validate(self, value: Any) -> None:
        """ Checks if the value is within bounds. """
        super().validate(value)
        self._validate_within_bounds(value)


class FloatBoundedProperty(BoundedProperty):
    """ Bounded property of type float. """

    def __init__(self, name, lower: float = None, upper: float = None) -> None:
        super().__init__(name, float, lower, upper)


class IntBoundedProperty(BoundedProperty):
    """ Bounded property of type int. """

    def __init__(self, name, lower: int = None, upper: int = None) -> None:
        super().__init__(name, int, lower, upper)
