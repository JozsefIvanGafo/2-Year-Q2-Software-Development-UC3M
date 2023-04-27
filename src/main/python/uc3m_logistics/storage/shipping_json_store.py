"""File containing the class ShipmentsJSONStore"""
import json
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.order_management_exception import OrderManagementException
from .json_store import JSONStore


class ShipmentsJSONStore(JSONStore):
    """ Class that contains function for the json file shipments_store"""
    class __ShipmentsJSONStore(JSONStore):
        def __init__(self):
            super().__init__()
            self._json_file_name = JSON_FILES_PATH + "shipments_store.json"


    instance = None

    def __new__(cls):
        if not ShipmentsJSONStore.instance:
            ShipmentsJSONStore.instance = ShipmentsJSONStore.__ShipmentsJSONStore()
        return ShipmentsJSONStore.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
