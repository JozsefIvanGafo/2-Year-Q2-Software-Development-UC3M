"""File containing the class DeliverJSONStore"""
from datetime import datetime
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from .json_store import JSONStore

#pylint: disable=too-few-public-methods
class DeliverJSONStore(JSONStore):
    """ Class that contains function for the json file shipments_delivered"""

    # pylint: disable=invalid-name
    class __DeliverJSONStore(JSONStore):
        def __init__(self):
            super().__init__()
            self._json_file_name = JSON_FILES_PATH + "shipments_delivered.json"

        def add(self,item):
            """Method that loads, then generate a dictionary and the save it on the json file"""
            self.load()
            # append the delivery info
            self._data_list.append(str(item))
            self._data_list.append(str(datetime.utcnow()))
            self.save()

    instance = None

    def __new__(cls):
        if not DeliverJSONStore.instance:
            DeliverJSONStore.instance = DeliverJSONStore.__DeliverJSONStore()
        return DeliverJSONStore.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
