""" FILE CONTAING THE CLASS ORDERtYPE"""
from .attribute import Attribute
#pylint: disable=too-few-public-methods
class OrderType(Attribute):
    """class containg the ordertypes atributes"""
    def __init__(self, attr_value):
        self._error_message = "order_type is not valid"
        self._validation_pattern = r"(Regular|Premium)"
        self._attr_value = self._validate(attr_value)
