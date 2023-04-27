"""   File containing the Attribute class that will be used as a blueprint for all the attributes"""
import re
from ..order_management_exception import OrderManagementException

class Attribute():
    """ Class that contains a function where it validates a certain value"""
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self,value):
        """ Function that checks if it match validation patern with the value"""
        myregex = re.compile(self._validation_pattern)
        match = myregex.fullmatch(value)
        if not match:
            raise OrderManagementException(self._error_message)
        return value

    @property
    def value(self):
        """It returns the value self._attr_value"""
        return self._attr_value
    @value.setter
    def value(self,value):
        self._attr_value = self._validate(value)

    def __str__(self):
        return self._attr_value
