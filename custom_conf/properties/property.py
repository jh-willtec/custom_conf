""" Descriptors for the properties of the Config.

This is to enable a 'Config.some_property'-lookup, without the
need to hard-code each property.
"""

from __future__ import annotations

from typing import (Any, TYPE_CHECKING, TypeVar)

import custom_conf.errors as err


if TYPE_CHECKING:
    from config import InstanceDescriptorMixin  # noqa: F401

CType = TypeVar("CType", bound="InstanceDescriptorMixin")


class Property:
    """ Base class for config properties. """

    def __init__(self, name: str, attr_type: type) -> None:
        self.cls: CType | None = None
        self.name: str = name
        self.attr: str = "__" + name
        self.type: type = attr_type

    def __get__(self, obj: CType, objtype=None) -> Any:
        try:
            return getattr(obj, self.attr)
        except AttributeError:
            raise err.MissingRequiredPropertyError(prop=self)

    def __set__(self, obj, value: Any):
        self.validate(value)
        setattr(obj, self.attr, value)

    def _raise_type_error(self, typ: type) -> None:
        raise err.InvalidPropertyTypeError(prop=self, type=typ)

    def _validate_type(self, value: Any) -> None:
        if isinstance(value, self.type):
            return
        raise err.InvalidPropertyTypeError(prop=self, type=type(value))

    def validate(self, value: Any) -> None:
        """ Check if there are any obvious errors with the value. """
        self._validate_type(value)

    def register(self, cls: CType) -> None:
        """ Ensure the instance using this property knows of its existence. """
        self.cls = cls
        self.cls.properties.append(self.name)
