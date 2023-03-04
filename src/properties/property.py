""" Descriptors for the properties of the Config.

This is to enable a 'Config.some_property'-lookup, without the
need to hard-code each property.
"""

from __future__ import annotations

import logging
from typing import (Any, TYPE_CHECKING, TypeVar)

import errors as err


if TYPE_CHECKING:
    from config import InstanceDescriptorMixin  # noqa: F401

logger = logging.getLogger(__name__)
CType = TypeVar("CType", bound="InstanceDescriptorMixin")


class Property:
    """ Base class for config properties. """

    def __init__(self, name: str, attr_type: type) -> None:
        self.cls = None
        self.name = name
        self.attr = "__" + name
        self.type = attr_type

    def __get__(self, obj: CType, objtype=None) -> Any:
        try:
            return getattr(obj, self.attr)
        except AttributeError:
            raise err.MissingRequiredPropertyError

    def __set__(self, obj, value: Any):
        self.validate(value)
        setattr(obj, self.attr, value)

    def _raise_type_error(self, typ: type) -> None:
        logger.error(f"Invalid config type for {self.name}. "
                     f"Expected '{self.type}', got '{typ}' instead.")
        raise err.InvalidPropertyTypeError

    def _validate_type(self, value: Any) -> None:
        if isinstance(value, self.type):
            return
        self._raise_type_error(type(value))

    def validate(self, value: Any) -> None:
        """ Check if there are any obvious errors with the value. """
        self._validate_type(value)

    def register(self, cls: CType) -> None:
        """ Ensure the instance using this property knows of its existence. """
        self.cls = cls
        self.cls.properties.append(self.name)
