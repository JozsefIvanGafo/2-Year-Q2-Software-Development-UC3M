"""Containing the blueprint for the Json store class"""
import json
from uc3m_logistics.order_management_exception import OrderManagementException

class JSONStore():
    """Function that has the default methods related to json files"""
    def __init__(self):
        self._json_file_name = ""
        self._data_list = []

    def load(self):
        """
        Method that loads what is inside the json file into data list
        :param self:
        :return: NONE
        """
        try:
            with open(self._json_file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            self._data_list = []
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error

    def save(self):
        """Method that saves what is inside of data list into the json file"""
        try:
            with open(self._json_file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as my_error:
            raise OrderManagementException("Wrong file or file path") from my_error

    def find(self,key,value):
        """Method that finds a value inside data_list"""
        self.load()
        for item in self._data_list:
            if item[key] == value:
                return item
        return None

    def add(self, item):
        """Method that loads, then generate a dictionary and the save it on the json file"""
        self.load()
        self._data_list.append(item.__dict__)
        self.save()
    @property
    def data_list(self):
        """Protect the data list and make it
        read only for the user"""
        return self._data_list
