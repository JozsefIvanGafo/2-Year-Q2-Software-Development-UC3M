"""Module """
import datetime
import re
import json
from datetime import datetime
from freezegun import freeze_time
from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping
from .order_manager_config import JSON_FILES_PATH

class OrderManager:
    """Class for providing the methods for managing the orders process"""
    def __init__(self):
        pass

    @staticmethod
    def validate_ean13( ean13 ):
        """method vor validating a ean13 code"""
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE EAN13
        # RETURN TRUE IF THE EAN13 IS RIGHT, OR FALSE IN OTHER CASE
        checksum = 0
        code_read = -1
        is_valid = False
        regex_ean13 = re.compile("^[0-9]{13}$")
        valid_ean13_format = regex_ean13.fullmatch(ean13)
        if valid_ean13_format is None:
            raise OrderManagementException("Invalid EAN13 code string")

        for position, digit in enumerate(reversed(ean13)):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if position == 0:
                code_read = current_digit
            else:
                checksum += (current_digit) * 3 if (position % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10

        if (code_read != -1) and (code_read == control_digit):
            is_valid = True
        else:
            raise OrderManagementException("Invalid EAN13 control digit")
        return is_valid

    @staticmethod
    def validate_tracking_code(tracking_code):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        match = myregex.fullmatch(tracking_code)
        if not match:
            raise OrderManagementException("tracking_code format is not valid")

    @staticmethod
    def save_order(order):
        """Medthod for saving the orders store"""
        orders_store = JSON_FILES_PATH + "orders_store.json"
        #first read the file
        try:
            with open(orders_store, "r", encoding="utf-8", newline="") as file:
                order_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            order_list = []
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error

        found = False
        for item in order_list:
            if item["_OrderRequest__order_id"] == order.order_id:
                found = True
        if found is False:
            order_list.append(order.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")
        try:
            with open(orders_store, "w", encoding="utf-8", newline="") as file:
                json.dump(order_list, file, indent=2)
        except FileNotFoundError as my_error:
            raise OrderManagementException("Wrong file or file path") from my_error
        return True

    @staticmethod
    def save_fast(data):
        """Method for saving the orders store"""
        orders_store = JSON_FILES_PATH + "orders_store.json"
        with open(orders_store, "r+", encoding="utf-8", newline="") as file:
            order_list = json.load(file)
            order_list.append(data.__dict__)
            file.seek(0)
            json.dump(order_list, file, indent=2)

    @staticmethod
    def save_orders_shipped( shipment ):
        """Saves the shipping object into a file"""
        shimpents_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shimpents_store_file, "r", encoding="utf-8", newline="") as file:
                #change misterious name to shipping_list
                shipping_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my shipping_list
            shipping_list = []
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error

        #append the shipments list
        shipping_list.append(shipment.__dict__)

        try:
            with open(shimpents_store_file, "w", encoding="utf-8", newline="") as file:
                json.dump(shipping_list, file, indent=2)
        except FileNotFoundError as my_error:
            raise OrderManagementException("Wrong file or file path") from my_error


    #pylint: disable=too-many-arguments
    def register_order( self, product_id,
                        order_type,
                        address,
                        phone_number,
                        zip_code ):
        """Register the orders into the order's file"""

        if self.validate_ean13(product_id):
            my_order = OrderRequest(product_id,
                                    order_type,
                                    address,
                                    phone_number,
                                    zip_code)

        self.save_order(my_order)

        return my_order.order_id



    #pylint: disable=too-many-locals
    def send_product ( self, input_file ):
        """Sends the order included in the input_file"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as my_error:
            # file is not found
            raise OrderManagementException("File is not found") from my_error
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error

        #check all the information
        try:
            myregex = re.compile(r"[0-9a-fA-F]{32}$")
            match = myregex.fullmatch(data["OrderID"])
            if not match:
                raise OrderManagementException("order id is not valid")
        except KeyError as my_error:
            raise  OrderManagementException("Bad label") from my_error

        try:
            regex_email = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
            myregex = re.compile(regex_email)
            match = myregex.fullmatch(data["ContactEmail"])
            if not match:
                raise OrderManagementException("contact email is not valid")
        except KeyError as my_error:
            raise OrderManagementException("Bad label") from my_error
        file_store = JSON_FILES_PATH + "orders_store.json"

        with open(file_store, "r", encoding="utf-8", newline="") as file:
            order_list = json.load(file)
        found = False
        for item in order_list:
            if item["_OrderRequest__order_id"] == data["OrderID"]:
                found = True
                #retrieve the orders data
                product_id = item["_OrderRequest__product_id"]
                address = item["_OrderRequest__delivery_address"]
                reg_type = item["_OrderRequest__order_type"]
                phone = item["_OrderRequest__phone_number"]
                order_timestamp = item["_OrderRequest__time_stamp"]
                zip_code = item["_OrderRequest__zip_code"]
                #set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = OrderRequest(product_id=product_id,
                                         delivery_address=address,
                                         order_type=reg_type,
                                         phone_number=phone,
                                         zip_code=zip_code)

                if order.order_id != data["OrderID"]:
                    raise OrderManagementException("Orders' data have been manipulated")

        if not found:
            raise OrderManagementException("order_id not found")

        my_sign= OrderShipping(product_id=product_id,
                               order_id=data["OrderID"],
                               order_type=reg_type,
                               delivery_email=data["ContactEmail"])

        #save the OrderShipping in shipments_store.json

        self.save_orders_shipped(my_sign)

        return my_sign.tracking_code

    def deliver_product( self, tracking_code ):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)

        #check if this tracking_code is in shipments_store
        shimpents_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shimpents_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error
        except FileNotFoundError as my_error:
            raise OrderManagementException("shipments_store not found") from my_error
        #search this tracking_code
        found = False
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == tracking_code:
                found = True
                del_timestamp = item["_OrderShipping__delivery_day"]
        if not found:
            raise OrderManagementException("tracking_code is not found")

        today= datetime.today().date()
        delivery_date= datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

        shipments_file = JSON_FILES_PATH + "shipments_delivered.json"

        try:
            with open(shipments_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as my_error:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as my_error:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from my_error

            # append the delivery info
        data_list.append(str(tracking_code))
        data_list.append(str(datetime.utcnow()))
        try:
            with open(shipments_file, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as my_error:
            raise OrderManagementException("Wrong file or file path") from my_error
        return True
