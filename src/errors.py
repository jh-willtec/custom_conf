""" Exceptions raised by properties. """
from typing import Any, TypeVar


INVALID_CONFIG_EXIT_CODE = 1


class PropertyError(Exception):
    """ Base class for exceptions raised by properties. """
    pass


class InvalidPropertyTypeError(PropertyError):
    """ Raised, if the type of a value differs from the properties type. """
    pass


class MissingRequiredPropertyError(PropertyError):
    """ Raised, if a required property is missing.
    Currently all properties are required. """
    pass


BP = TypeVar("BP", bound="prop")


class OutOfBoundsPropertyError(PropertyError):
    """ Raised, if the given value of a bounded property is out of bounds. """
    def __init__(self, prop: BP, value) -> None:
        prop_type_name = prop.__class__.__name__
        msg = (f"The given value '{value} for the {prop_type_name} "
               f"'{prop.name}' is out of bounds [{prop.lower}, {prop.upper}].")
        super().__init__(msg)


class IncomparableBoundsTypeError(PropertyError):
    def __init__(self, typ: type) -> None:
        msg = (f"The given type {typ} is not comparable and can not be used "
               f"as bounds.")
        super().__init__(msg)


class MissingBoundsError(PropertyError):
    def __init__(self) -> None:
        super().__init__("Either a lower or an upper bound is required!")


class InvalidBoundsError(PropertyError):
    def __init__(self, which: str, expected_type: type, value: Any) -> None:
        msg = (f"The {which} bound with value '{value}' is not of the "
               f"expected type '{expected_type}'.")
        super().__init__(msg)


class InvalidLowerBoundsError(InvalidBoundsError):
    def __init__(self, expected_type: type, value: Any) -> None:
        super().__init__("lower", expected_type, value)


class InvalidUpperBoundsError(InvalidBoundsError):
    def __init__(self, expected_type: type, value: Any) -> None:
        super().__init__("upper", expected_type, value)


class UnknownPropertyError(PropertyError):
    """ Raised, when trying to set a property that does not exist.
    Usually this happens, when the name was missspelled. """
    pass
