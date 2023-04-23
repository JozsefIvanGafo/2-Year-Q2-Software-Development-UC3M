""" File containing the class zip code"""
from .attribute import Attribute
from ..order_management_exception import OrderManagementException
#pylint: disable=too-few-public-methods

class ZipCode(Attribute):
    """Class that verifies the zip cod eattribure"""
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "zip_code format is not valid"
        self._validation_pattern = "^[0-9]{5}$"
        self._attr_value = self._validate(attr_value)
    def _validate(self, value):
        """Function that inherits the function validate
        from attributes and checks if the zip code is valñid or not"""
        super()._validate(value)
        if (int(value) > 52999 or int(value) < 1000):
            raise OrderManagementException("zip_code is not valid")
        return value
