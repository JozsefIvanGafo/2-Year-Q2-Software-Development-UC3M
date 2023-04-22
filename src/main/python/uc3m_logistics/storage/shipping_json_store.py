from .json_store import JSONStore
import json
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.order_management_exception import OrderManagementException

class ShipmentsJSONStore(JSONStore):
    def __init__(self):
        super().__init__()
        self._json_file_name = JSON_FILES_PATH + "shipments_store.json"
    def add(self,item):
        super().add(item)

