import json
from uc3m_logistics.order_management_exception import OrderManagementException

class JSONStore():
    def __init__(self):
        self._json_file_name = ""
        self._data_list = []

    def load(self):
        try:
            with open(self._json_file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            self._data_list = []
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error




    def save(self):
        try:
            with open(self._json_file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as my_error:
            raise OrderManagementException("Wrong file or file path") from my_error

    def find(self,key,value):
        self.load()
        for item in self._data_list:
            if item[key] == value:
                return item
        return None

    def add(self, item):
        self.load()
        self._data_list.append(item.__dict__)
        self.save()
