from __future__ import annotations

from types import UnionType
from typing import Any, get_args, get_origin, Iterable, Union

import custom_conf.errors as err
from custom_conf.properties.property import Property


# TODO: This needs more explaining.
def value_to_generic(base_value: Any) -> type:
    """ Returns the generic type of a given value. """

    def get_dict_item_types() -> tuple[slice]:
        """ Return the types of the base_value, if base_value is a dict. """
        item_types: dict[type: type] = {}
        for key, value in base_value.items():
            key_type = value_to_generic(key)
            value_type = value_to_generic(value)
            item_types.setdefault(key_type, value_type)
            item_types[key_type] |= value_type
        return tuple([slice(key, value) for key, value in item_types.items()])

    def get_iter_item_types() -> Union[type]:
        """ Return the types of the base_value, if base_value is a list. """
        item_types: set[type] = set()
        for value in base_value:
            item_types.add(value_to_generic(value))
        typ = item_types.pop()
        for item_type in item_types:
            typ |= item_type
        return typ

    base_type = type(base_value)
    # Need to check str first, because it is an Iterable but not a Generic.
    if base_type is str:
        return base_type
    if base_type is dict:
        return base_type.__class_getitem__(get_dict_item_types())
    if isinstance(base_value, Iterable) and base_value:
        return base_type.__class_getitem__(get_iter_item_types())
    return base_type


class NestedTypeProperty(Property):
    """ Base class used by properties, which have a nested or generic type.
    This is necessary, because isinstance() does not work with Generics. """

    def _validate_type(self, value: Any) -> None:
        try:
            self._validate_generic_type(value, self.type)
        except err.InvalidPropertyTypeError:
            raise err.InvalidPropertyTypeError(prop=self, type=type(value))

    def _validate_generic_type(self, value: Any, typ: type) -> None:
        # TODO: Document this properly.
        if typ is None:
            return
        origin = get_origin(typ)
        if origin is None:
            if not isinstance(value, typ):
                raise err.InvalidPropertyTypeError
            return
        if origin not in [Union, UnionType]:
            self._validate_generic_type(value, origin)
        if origin is dict:
            self._validate_generic_dict(value, typ)
        elif isinstance(origin, Iterable):
            self._validate_generic_iterable(value, typ)
        else:
            self._validate_generic_type_args(value, typ)

    def _validate_generic_dict(self, value: Any, typ: type) -> None:
        args = get_args(typ)
        for key, val in value.items():
            valid = False
            for arg in args:
                try:
                    if isinstance(arg, slice):
                        self._validate_generic_type(key, arg.start)
                        self._validate_generic_type(val, arg.stop)
                        valid = True
                        continue
                    self._validate_generic_type(key, arg)
                    self._validate_generic_type(val, arg)
                    valid = True
                except err.InvalidPropertyTypeError:
                    pass
            if not valid:
                raise err.InvalidPropertyTypeError

    def _validate_generic_iterable(self, value: Any, typ: type) -> bool:
        args = get_args(typ)
        for key, val in value:
            valid = True
            for arg in args:
                if isinstance(arg, slice):
                    valid |= self._validate_generic_type(val, arg.start)
                    valid |= self._validate_generic_type(val, arg.start)
                    continue
                valid |= self._validate_generic_type(val, arg)
            if not valid:
                return False

    def _validate_generic_type_args(self, value: Any, typ: type) -> None:
        args = get_args(typ)
        if not args:
            return
        try:
            for val in value:
                valid = False
                for arg in args:
                    try:
                        self._validate_generic_type(val, arg)
                        valid = True
                        break
                    except err.InvalidPropertyTypeError:
                        pass
                if not valid:
                    raise err.InvalidPropertyTypeError
        except TypeError:
            pass


class IntListProperty(NestedTypeProperty):
    def __init__(self, attr) -> None:
        super().__init__(attr, list[int])
