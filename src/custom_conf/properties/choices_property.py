from typing import Any

from custom_conf.properties.property import Property
import custom_conf.errors as err


class ChoicesProperty(Property):
    def __init__(self, name: str, attr_type: type, choice: list) -> None:
        super().__init__(name, attr_type)
        self._choices = choice
        self.validate_choices_type()

    @property
    def choices(self) -> list:
        return self._choices

    def validate_choices_type(self) -> None:
        if any(map(lambda c: not isinstance(c, self.type), self.choices)):
            raise err.InvalidChoicesTypeError(self)

    def validate(self, value: Any) -> None:
        super().validate(value)
        if value not in self.choices:
            raise err.InvalidChoiceError
