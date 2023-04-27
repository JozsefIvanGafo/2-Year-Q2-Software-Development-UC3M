"""Class that contains the class SendInput"""
import json
from .attributes.attribute_contact_email import ContactEmail
from .attributes.attribute_order_id import OrderID
from .order_management_exception import OrderManagementException
from .storage.json_store import JSONStore

class SendInput(JSONStore):
    """Class that inherits JsonStore and has method srelated with json files"""
    __send_data = None
    def __init__(self,input_file):
        super().__init__()
        #input_file = JSON_FILES_PATH + "shipments_store.json"
        self._get_data_from_input_file(input_file)
        self._order_id = OrderID(self.__send_data["OrderID"]).value
        self._contact_email = ContactEmail(self.__send_data["ContactEmail"]).value

    def _get_data_from_input_file(self, input_file):
        """Method that opens an input file and then validate it"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                self.__send_data = json.load(file)
        except FileNotFoundError as my_error:
            # file is not found
            raise OrderManagementException("File is not found") from my_error
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error
        self._validate_label()

    def _validate_label(self):
        """Method to validate the labels OrderID and contactEmail"""
        if "OrderID" in self.__send_data.keys() and "ContactEmail" in self.__send_data.keys():
            return True
        raise OrderManagementException("Bad label")

    @property
    def order_id(self):
        """It returns the value self._order_id"""
        return self._order_id

    @property
    def contact_email(self):
        """It returns the value self._contact_email"""
        return self._contact_email
