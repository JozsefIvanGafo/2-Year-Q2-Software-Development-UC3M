""" File containing the class productId"""
from .attribute import Attribute
from ..order_management_exception import OrderManagementException
#pylint: disable=too-few-public-methods
class ProductId(Attribute):
    """Class containg the validate function of the product id"""
    def __init__(self,attr_value):
        super().__init__()
        self._validation_pattern = "^[0-9]{13}$"
        self._error_message = "Invalid EAN13 code string"
        self._attr_value = self._validate(attr_value)

    def _validate(self, value):
        """method vor validating a ean13 code"""
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE EAN13
        # RETURN TRUE IF THE EAN13 IS RIGHT, OR FALSE IN OTHER CASE
        super()._validate(value)
        checksum = 0
        code_read = -1
        for position, digit in enumerate(reversed(value)):
            try:
                current_digit = int(digit)
            except ValueError as my_error:
                raise OrderManagementException("Invalid EAN13 code string") from my_error
            if position == 0:
                code_read = current_digit
            else:
                checksum += (current_digit) * 3 if (position % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10

        if (code_read == -1) or (code_read != control_digit):
            raise OrderManagementException("Invalid EAN13 control digit")
        return value
