""" Class containing the address atribute """
from .attribute import Attribute

#pylint: disable=too-few-public-methods
class TrackingCode(Attribute):
    """ Class containing the Tracking code attributes """
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "tracking_code format is not valid"
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._attr_value = self._validate(attr_value)
