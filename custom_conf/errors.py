""" Exceptions raised by properties. """
from typing import Any


INVALID_CONFIG_EXIT_CODE = 1
# TODO: Bind the arguments the exceptions were called with to the
#  instance, to make them available to error handling.


class CustomConfError(Exception):
    """ Base class for any custom exceptions raised by custom_conf. """
    pass


class ConfigError(CustomConfError):
    """ Base class for exceptions raised by the config. """
    pass


class AddAfterInitError(ConfigError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when a new property is added to the configuration, after
        the config was initialized.

        :keyword name: The name of the property.
        :type name: str
        """
        infix = f", with name '{kwargs['name']}'," if "name" in kwargs else ""
        super().__init__(
            f"Tried adding a new property{infix} to the configuration.")


class PropertyError(CustomConfError):
    """ Base class for exceptions raised by properties. """
    pass


class MismatchedPropertyNameError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when the name used for a property and the variable
        name in the config of the same property are different.

        :keyword prop: The property that was created.
        :type prop: Property
        :keyword name: The name that is used in the Config.
        :type name: str
        """
        if "prop" not in kwargs or "name" not in kwargs:
            super().__init__()
            return
        prop_name = kwargs["prop"].name
        name = kwargs["name"]
        msg = (f"The property with the name '{prop_name}' is used "
               f"for the configuration key '{name}'. Property name and "
               f"config instance variable names have to be the equal.")
        super().__init__(msg)


class InvalidPropertyTypeError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, if the type of a value differs from the properties type.

        :keyword prop: The property that is being set.
        :type prop: Property
        :keyword type: The type of the value.
        :type type: type
        """
        if "prop" not in kwargs or "type" not in kwargs:
            super().__init__()
            return
        prop = kwargs["prop"]
        value_type = kwargs["type"]
        msg = (f"Invalid config type for property '{prop.name}'. "
               f"Expected '{prop.type}', got '{value_type}' instead.")
        super().__init__(msg)


class NotATypeError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """
        Raised, when the type provided to a property is not a type.

        :keyword type: The object that was provided as a type for the property.
        """
        if "type" not in kwargs:
            super().__init__()
            return
        prop_type = kwargs["type"]
        super().__init__(f"The provided type '{prop_type}' is not a type.")


class MissingRequiredPropertyError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, if a required property is missing.
        Currently all properties are required.

        :keyword prop: The property object that is missing a value.
        :type prop: A Property object
        """
        if "prop" not in kwargs:
            super().__init__()
            return
        prop = kwargs["prop"]
        # TODO: Make a difference between Missing and QueryBeforeSet?
        msg = (f"The property '{prop.name}' was not set before it was first "
               f"queried, even though it is a required property.")
        super().__init__(msg)


class UnknownPropertyError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when trying to set a property that does not exist.
        Usually this happens, when the name was missspelled.

        :keyword name: The name of the requested property.
        :type name: str
        :keyword value: The value the requested property would be set to.
        :type value: Any
        """
        if "key" not in kwargs or "value" not in kwargs:
            super().__init__()
            return
        key = kwargs["key"]
        value = kwargs["value"]
        msg = (f"An unknown property with the name '{key}' and "
               f"value '{value}' was requested.")
        super().__init__(msg)


###########################
# Bounded property errors #
###########################


class OutOfBoundsPropertyError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, if the given value of a bounded property is out of bounds.

        :keyword prop: The property that is being modified.
        :type prop: BoundedProperty
        :keyword value: The value the property is being set to.
        :type value: The type of the property (prop.type)
        """
        if "prop" not in kwargs or "value" not in kwargs:
            super().__init__()
            return
        prop = kwargs["prop"]
        value = kwargs["value"]
        prop_type_name = prop.__class__.__name__
        msg = (f"The given value '{value}' for the {prop_type_name} "
               f"'{prop.name}' is out of bounds [{prop.lower}, {prop.upper}].")
        super().__init__(msg)


class IncomparableBoundsTypeError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised when values with the properties type can not be compared.

        :keyword type: The type of the property that can not be compared.
        :type type: type
        """
        if "type" not in kwargs:
            super().__init__()
            return
        typ = kwargs["type"]
        msg = (f"The given type '{typ}' is not comparable and can thus not "
               f"be used as bounds.")
        super().__init__(msg)


class MissingBoundsError(PropertyError):
    def __init__(self) -> None:
        """ Raised when neither the lower nor upper bound were provided. """
        super().__init__("Either the lower or the upper bound is required!")


class _InvalidBoundsError(PropertyError):
    def __init__(self, which: str, expected_type: type, value: Any) -> None:
        msg = (f"The {which} bound with value '{value}' is not of the "
               f"expected type '{expected_type}'.")
        super().__init__(msg)


class InvalidLowerBoundsError(_InvalidBoundsError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when the lower bound is of the wrong type.

        :keyword type: The type that is expected.
        :type type: type
        :keyword value: The value that was provided as lower bound.
        :type value: Any
        """
        if "type" not in kwargs or "value" not in kwargs:
            super(Exception, self).__init__()
            return
        expected_type = kwargs["type"]
        value = kwargs["value"]
        super().__init__("lower", expected_type, value)


class InvalidUpperBoundsError(_InvalidBoundsError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when the upper bound is of the wrong type.

        :keyword type: The type that is expected.
        :type type: type
        :keyword value: The value that was provided as upper bound.
        :type value: Any
        """
        if "type" not in kwargs or "value" not in kwargs:
            super(Exception, self).__init__()
            return
        expected_type = kwargs["type"]
        value = kwargs["value"]
        super().__init__("upper", expected_type, value)


class InvalidBoundOrderError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when the lower bound is greater to the upper bound.

        :keyword name: The name of the property with wrong bounds.
        :type name: str
        """
        if "name" not in kwargs:
            super().__init__()
            return
        name = kwargs["name"]
        super().__init__(f"The lower bound of the '{name}' property is "
                         f"greater or equal to the upper bound.")
