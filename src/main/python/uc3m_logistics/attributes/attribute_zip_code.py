""" File containing the class zip code"""
from .attribute import Attribute
from ..order_management_exception import OrderManagementException
#pylint: disable=too-few-public-methods
class ZipCode(Attribute):
    """Class that verifies the zip cod eattribure"""
    def __init__(self, attr_value):
        self._error_message = "zip_code format is not valid"
        self._validation_pattern = "^[0-9]{5}$"
        self._attr_value = self._validate(attr_value)
    def _validate(self, attr_value):
        """Function that inherits the function validate
        from attributes and checks if the zip code is valñid or not"""
        super()._validate(attr_value)
        if attr_value.isnumeric() and len(attr_value) == 5:
            if (int(attr_value) > 52999 or int(attr_value) < 1000):
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")
        return attr_value
