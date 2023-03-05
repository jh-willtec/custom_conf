""" Exceptions raised by properties. """
from typing import Any, TypeVar, TYPE_CHECKING


if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from properties.property import Property
    # noinspection PyUnresolvedReferences
    from properties.bounded_property import BoundedProperty


INVALID_CONFIG_EXIT_CODE = 1
P = TypeVar("P", bound="Property")


class PropertyError(Exception):
    """ Base class for exceptions raised by properties. """
    pass


class InvalidPropertyTypeError(PropertyError):
    """ Raised, if the type of a value differs from the properties type. """
    def __init__(self, prop: P = None, value_type: type = None) -> None:
        msg = ""
        if prop is not None:
            msg = (f"Invalid config type for property '{prop.name}'. "
                   f"Expected '{prop.type}', got '{value_type}' instead.")
        super().__init__(msg)


class NotATypeError(PropertyError):
    def __init__(self, typ: Any) -> None:
        super().__init__(f"The provided type '{typ}' is not a type.")


class MissingRequiredPropertyError(PropertyError):
    """ Raised, if a required property is missing.
    Currently all properties are required. """
    def __init__(self, prop: P):
        # TODO: Make a difference between Missing and QueryBeforeSet?
        msg = (f"The property '{prop}' was not set before it was first "
               f"queried, even though it is a required property.")
        super().__init__(msg)


class UnknownPropertyError(PropertyError):
    """ Raised, when trying to set a property that does not exist.
    Usually this happens, when the name was missspelled. """
    def __init__(self, key: str, value: Any) -> None:
        msg = f"An unknown property with the name '{key}' was requested."
        super().__init__(msg)


###########################
# Bounded property errors #
###########################


BP = TypeVar("BP", bound="BoundedProperty")


class OutOfBoundsPropertyError(PropertyError):
    """ Raised, if the given value of a bounded property is out of bounds. """
    def __init__(self, prop: BP, value: Any) -> None:
        prop_type_name = prop.__class__.__name__
        msg = (f"The given value '{value}' for the {prop_type_name} "
               f"'{prop.name}' is out of bounds [{prop.lower}, {prop.upper}].")
        super().__init__(msg)


class IncomparableBoundsTypeError(PropertyError):
    def __init__(self, typ: type) -> None:
        msg = (f"The given type '{typ}' is not comparable and can thus not "
               f"be used as bounds.")
        super().__init__(msg)


class MissingBoundsError(PropertyError):
    def __init__(self) -> None:
        super().__init__("Either the lower or the upper bound is required!")


class _InvalidBoundsError(PropertyError):
    def __init__(self, which: str, expected_type: type, value: Any) -> None:
        msg = (f"The {which} bound with value '{value}' is not of the "
               f"expected type '{expected_type}'.")
        super().__init__(msg)


class InvalidLowerBoundsError(_InvalidBoundsError):
    def __init__(self, expected_type: type, value: Any) -> None:
        super().__init__("lower", expected_type, value)


class InvalidUpperBoundsError(_InvalidBoundsError):
    def __init__(self, expected_type: type, value: Any) -> None:
        super().__init__("upper", expected_type, value)


class InvalidBoundOrderError(PropertyError):
    def __init__(self, name) -> None:
        super().__init__(f"The lower bound of the '{name}' property is "
                         f"greater or equal to the upper bound.")

