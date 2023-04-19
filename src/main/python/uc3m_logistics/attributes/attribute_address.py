""" Class containing the address atribute """
from .attribute import Attribute

#pylint: disable=too-few-public-methods
class Address(Attribute):
    """ Class containing the address atributes """
    def __init__(self, attr_value):
        self._error_message = "address is not valid"
        self._validation_pattern = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self._attr_value = self._validate(attr_value)
