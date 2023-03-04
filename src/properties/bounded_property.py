from __future__ import annotations

from typing import Any

import errors as err
from properties.property import Property


class BoundsProperty(Property):
    """ Used for properties with bounded values. """

    def __init__(
            self, name: str, attr_type: type, lower=None, upper=None) -> None:
        super().__init__(name, attr_type)
        # Ensure the bounds are of the correct type.
        if lower is not None:
            self._validate_type(lower)
        if upper is not None:
            self._validate_type(upper)
        self.lower = lower
        self.upper = upper

    def _validate_within_bounds(self, value: Any):
        upper_oob = self.upper and value > self.upper
        lower_oob = self.lower and value < self.lower
        # TODO: Needs proper errors, if oob.
        if upper_oob or lower_oob:
            raise err.OutOfBoundsPropertyError

    def validate(self, value: Any) -> None:
        """ Checks if the value is within bounds. """
        super().validate(value)
        self._validate_within_bounds(value)


class FloatBoundsProperty(BoundsProperty):
    """ Bounded property of type float. """

    def __init__(self, name, lower: float = None, upper: float = None) -> None:
        super().__init__(name, float, lower, upper)


class IntBoundsProperty(BoundsProperty):
    """ Bounded property of type int. """

    def __init__(self, name, lower: int = None, upper: int = None) -> None:
        super().__init__(name, int, lower, upper)
