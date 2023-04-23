"""File containing the class ShipmentsJSONStore"""
import json
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.order_management_exception import OrderManagementException
from .json_store import JSONStore


class ShipmentsJSONStore(JSONStore):
    """ Class that contains function for the json file shipments_store"""
    def __init__(self):
        super().__init__()
        self._json_file_name = JSON_FILES_PATH + "shipments_store.json"
    def find(self,key,value):
        """Method that finds a value inside data_list else it raises an exception"""
        self.load_shipment()
        for item in self._data_list:
            if item[key] == value:
                return item
        raise OrderManagementException("tracking_code is not found")

    def load_input_file(self,input_file):
        """
        Method that loads what is inside the input json file
        into data list , if it is empty it raises an error
        :param input_file: a json file
        :return:
        """

        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as my_error:
            # file is not found
            raise OrderManagementException("File is not found") from my_error
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error

    def load_shipment(self):
        """
        Method that loads what is inside the shipments_store
        json file into data list , if it is empty it raises an error
        :return:
        """
        try:
            with open(self._json_file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error
        except FileNotFoundError as my_error:
            raise OrderManagementException("shipments_store not found") from my_error
