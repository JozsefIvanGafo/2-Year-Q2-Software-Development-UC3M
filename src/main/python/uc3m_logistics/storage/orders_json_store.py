"""File containing the class OrdersJSONStore"""
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.order_management_exception import OrderManagementException
from .json_store import JSONStore

#pylint: disable=too-few-public-methods
class OrdersJSONStore(JSONStore):
    """ Class that contains function for the json file orders_store"""
    def __init__(self):
        super().__init__()
        self._json_file_name = JSON_FILES_PATH + "orders_store.json"

    def add(self, item):
        """Method that checks if OrderRequest_order ID exist and then loads, after generate a
        dictionary and the save it on the json file"""
        found = self.find("_OrderRequest__order_id",item.order_id)
        if found:
            raise OrderManagementException("order_id is already registered in orders_store")
        super().add(item)
