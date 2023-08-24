""" Exceptions raised by properties. """
from typing import Any


INVALID_CONFIG_EXIT_CODE = 1


class CustomConfError(Exception):
    """ Base class for any custom exceptions raised by custom_conf. """
    pass


class ConfigReaderError(CustomConfError):
    """ Base class for exceptions that occur when reading a configuration. """
    def __init__(self, **kwargs) -> None:
        self.path = kwargs.pop("path")
        msg = f"Could not read the configuration at '{self.path}'."
        super().__init__(msg)


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
        self.name = kwargs.get("name")
        infix = f", with name '{self.name}'," if self.name is not None else ""
        super().__init__(
            f"Tried adding a new property{infix} after the configuration "
            f"was initialized.")


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
        self.prop = kwargs.get("prop")
        self.name = kwargs.get("name")
        if "prop" not in kwargs or "name" not in kwargs:
            super().__init__()
            return
        msg = (f"The property with the name '{self.prop.name}' is used "
               f"for the configuration key '{self.name}'. Property name and "
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
        self.prop = kwargs.get("prop")
        self.type = kwargs.get("type")
        if "prop" not in kwargs or "type" not in kwargs:
            super().__init__()
            return
        msg = (f"Invalid config type for property '{self.prop.name}'. "
               f"Expected '{self.prop.type}', got '{self.type}' instead.")
        super().__init__(msg)


class InvalidCoercionError(PropertyError):
    def __init__(self, **kwargs) -> None:
        self.prop = kwargs.pop("prop")
        self.value = kwargs.pop("value")
        msg = (f"Could not cleanly coerce the value '{self.value}' "
               f"of type '{type(self.value)}' to type '{self.prop.type}' "
               f"for property '{self.prop.name}'.")
        super().__init__(msg)


class LossOfPrecisionError(PropertyError):
    def __init__(self, **kwargs) -> None:
        self.type = kwargs.pop("type")
        self.value = kwargs.pop("value")
        msg = (f"Coercion of '{self.value}' to type "
               f"'{self.type}' would reduce precision.")
        super().__init__(msg)


class NotATypeError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """
        Raised, when the type provided to a property is not a type.

        :keyword type: The object that was provided as a type for the property.
        """
        self.type = kwargs.get("type")
        if "type" not in kwargs:
            super().__init__()
            return
        super().__init__(f"The provided type '{self.type}' is not a type.")


class MissingRequiredPropertyError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, if a required property is missing.
        Currently all properties are required.

        :keyword prop: The property object that is missing a value.
        :type prop: A Property object
        """
        self.prop = kwargs.get("prop")
        if "prop" not in kwargs:
            super().__init__()
            return
        msg = (f"The property '{self.prop.name}' was not set during the "
               f"initialization, even though it is a required property.")
        super().__init__(msg)


class QueriedBeforeSetError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """"""
        self.prop = kwargs.get("prop")
        msg = (f"The property '{self.prop.name}' was queried "
               f"before it was assigned a value.")
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
        self.name = kwargs.get("name")
        self.value = kwargs.get("value")
        if "name" not in kwargs or "value" not in kwargs:
            super().__init__()
            return
        msg = (f"An unknown property with the name '{self.name}' and "
               f"value '{self.value}' was requested.")
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
        self.prop = kwargs.get("prop")
        self.value = kwargs.get("value")
        if "prop" not in kwargs or "value" not in kwargs:
            super().__init__()
            return
        prop_type_name = self.prop.__class__.__name__
        msg = (f"The given value '{self.value}' for the {prop_type_name} "
               f"'{self.prop.name}' is out of bounds "
               f"[{self.prop.lower}, {self.prop.upper}].")
        super().__init__(msg)


class IncomparableBoundsTypeError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised when values with the properties type can not be compared.

        :keyword type: The type of the property that can not be compared.
        :type type: type
        """
        self.type = kwargs.get("type")
        if "type" not in kwargs:
            super().__init__()
            return
        msg = (f"The given type '{self.type}' is not comparable and can "
               f"thus not be used as bounds.")
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
        self.type = kwargs.get("type")
        self.value = kwargs.get("value")
        if "type" not in kwargs or "value" not in kwargs:
            super(Exception, self).__init__()
            return
        super().__init__("lower", self.type, self.value)


class InvalidUpperBoundsError(_InvalidBoundsError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when the upper bound is of the wrong type.

        :keyword type: The type that is expected.
        :type type: type
        :keyword value: The value that was provided as upper bound.
        :type value: Any
        """
        self.type = kwargs.get("type")
        self.value = kwargs.get("value")
        if "type" not in kwargs or "value" not in kwargs:
            super(Exception, self).__init__()
            return
        super().__init__("upper", self.type, self.value)


class InvalidBoundOrderError(PropertyError):
    def __init__(self, **kwargs) -> None:
        """ Raised, when the lower bound is greater to the upper bound.

        :keyword name: The name of the property with wrong bounds.
        :type name: str
        """
        self.name = kwargs.get("name")
        if "name" not in kwargs:
            super().__init__()
            return
        super().__init__(f"The lower bound of the '{self.name}' "
                         f"property is greater or equal to the upper bound.")
