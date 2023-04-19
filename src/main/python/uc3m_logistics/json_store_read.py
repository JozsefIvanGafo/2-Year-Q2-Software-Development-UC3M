""" File containing the class JsonStoreRead"""
import json
from .order_manager_config import JSON_FILES_PATH
from .order_management_exception import OrderManagementException

class JsonStoreRead():
    """ Class conatining methods that are related with json files"""
    def __int__(self):
        pass
    @staticmethod
    def dump_json(data_list,path):
        """
        Method to dumop data on a json file
        :param data_list: a list containing the data that you want to dump
        :param path: the path of the json file
        :return: none
        """
        try:
            with open(path, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as my_error:
            raise OrderManagementException("Wrong file or file path") from my_error

    @staticmethod
    def read_json(input_file):
        """
        Method that read an json file
        :param input_file: The json file path
        :return: data_list (containing the data from the json file)
        """
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error
        return data_list
    @staticmethod
    def read_send_product(input_file):
        """
        Method that reads the send product json file
        :param input_file: the path of the json file
        :return: data (containing the data from the json file)
        """
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as my_error:
            # file is not found
            raise OrderManagementException("File is not found") from my_error
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error
        return data

    @staticmethod
    def read_shipments(input_file):
        """
        Reads the shipments file
        :param input_file: the path of the json file
        :return: data_list (containing the data from the json file)
        """
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error
        except FileNotFoundError as my_error:
            raise OrderManagementException("shipments_store not found") from my_error
        return data_list

    @staticmethod
    def save_order(order):
        """Medthod for saving the orders store"""
        orders_store = JSON_FILES_PATH + "orders_store.json"
        # first read the file
        order_list = JsonStoreRead.read_json(orders_store)
        found = False
        for item in order_list:
            if item["_OrderRequest__order_id"] == order.order_id:
                found = True
        if found is False:
            order_list.append(order.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")
        JsonStoreRead.dump_json(order_list, orders_store)
        return True


    @staticmethod
    def save_orders_shipped(shipment):
        """Saves the shipping object into a file"""
        shimpents_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        shipping_list=JsonStoreRead.read_json(shimpents_store_file)

        # append the shipments list
        shipping_list.append(shipment.__dict__)
        JsonStoreRead.dump_json(shipping_list, shimpents_store_file)
