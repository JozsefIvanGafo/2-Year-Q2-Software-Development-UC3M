"""from .attributes.attribute_contact_email import ContactEmail
from .attributes.attribute_order_id import OrderID
import json
from order_management_exception import OrderManagementException
from order_manager_config import JSON_FILES_PATH
from .storage.json_store import JSONStore
from .order_request import OrderRequest
from .order_shipping import OrderShipping
class SendInput(JSONStore):
    def __init__(self):
        input_file = JSON_FILES_PATH + "shipments_store.json"
        data = self.get_data_from_input_file(input_file)
        self._order_id = OrderID(data["OrderID"]).value
        self._contact_email = ContactEmail(data["ContactEmail"]).value

    def get_data_from_input_file(self, input_file):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as my_error:
            # file is not found
            raise OrderManagementException("File is not found") from my_error
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error

    def validate_label(self):
        if "OrderID" in self._data_list.keys() and "ContactEmail" in self._data_list.keys():
            return True
        raise OrderManagementException("Bad label")

    def get_order_shipping(self):
        order = OrderRequest.get_order_by_order_id()
        my_order_shipping = OrderShipping(product_id=order.product_id,
                                    order_id=order.order_id,
                                    order_type=order.order_type,
                                    delivery_email=self._contact_email)
        return my_order_shipping"""