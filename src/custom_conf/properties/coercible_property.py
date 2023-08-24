from typing import Any, Callable, TypeVar

from custom_conf.properties.property import Property
import custom_conf.errors as err


T = TypeVar("T")


def str_to_float(value: str) -> float:
    return float(value)


def float_to_int(value: float) -> int:
    if value.is_integer():
        return int(value)
    raise err.LossOfPrecisionError(type=int, value=value)


def str_to_int(value: str) -> int:
    return float_to_int(str_to_float(value))


class CoercableProperty(Property):
    def __init__(self,
                 name: str,
                 attr_type: T,
                 converter: dict[type: Callable[[Any], T]]) -> None:
        super().__init__(name, attr_type)
        self.converter = converter

    def _coerce(self, value: Any) -> T:
        try:
            return self.converter[type(value)](value)
        except err.PropertyError as e:
            raise err.InvalidCoercionError(prop=self, value=value) from e
        except (TypeError, ValueError, OverflowError):
            pass
        raise err.InvalidCoercionError(prop=self, value=value)

    def coerce_if_coercible(self, value: Any) -> T:
        if isinstance(value, self.type):
            return value
        if isinstance(value, tuple(self.converter.keys())):
            return self._coerce(value)
        raise err.InvalidPropertyTypeError(prop=self, type=type(value))

    def __set__(self, obj, raw_value: Any) -> None:
        value: T = self.coerce_if_coercible(raw_value)
        super().__set__(obj, value)


class IntProperty(CoercableProperty):
    def __init__(self, name) -> None:
        converter = {float: float_to_int, str: str_to_int}
        super().__init__(name, int, converter)


class FloatProperty(CoercableProperty):
    def __init__(self, name) -> None:
        converter = {int: float, str: str_to_float}
        super().__init__(name, float, converter)
