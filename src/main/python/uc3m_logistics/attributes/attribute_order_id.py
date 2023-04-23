""" Class containing the address atribute """
from .attribute import Attribute

#pylint: disable=too-few-public-methods
class OrderID(Attribute):
    """ Class containing the orderID attributes """
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "order id is not valid"
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._attr_value = self._validate(attr_value)
