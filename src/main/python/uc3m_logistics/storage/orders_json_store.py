from .json_store import JSONStore
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.order_management_exception import OrderManagementException

class OrdersJSONStore(JSONStore):
    def __init__(self):
        super().__init__()
        self._json_file_name = JSON_FILES_PATH + "orders_store.json"

    def add(self, item):
        found = self.find("_OrderRequest__order_id",item.order_id)
        if found:
            raise OrderManagementException("order_id is already registered in orders_store")
        super().add(item)