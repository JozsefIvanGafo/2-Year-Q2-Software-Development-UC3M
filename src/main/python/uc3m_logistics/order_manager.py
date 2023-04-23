"""Module """
import datetime
import re
from datetime import datetime
from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping
from .storage.orders_json_store import OrdersJSONStore
from .storage.shipping_json_store import ShipmentsJSONStore
from .storage.deliver_json_store import DeliverJSONStore
from .attributes.attribute_tracking_code import TrackingCode

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

    #pylint: disable=too-many-arguments
    def register_order( self, product_id,
                        order_type,
                        address,
                        phone_number,
                        zip_code ):
        """Method that registers and order and verifies its parameters"""
        #We define an object of OrdersJSONStore
        orders_json_store = OrdersJSONStore()

        #We validate and we create an object of OrderRequest
        if self.validate_ean13(product_id):
            my_order = OrderRequest(product_id,
                                    order_type,
                                    address,
                                    phone_number,
                                    zip_code)

        #Load and store the information of my_order into orders_store.json
        orders_json_store.add(my_order)
        #we return my order id of the product
        return my_order.order_id

    def validate_label(self,data):
        """
        Method that checks if the keys orderid and contactmail exist in data
        :param data: is a dictionary
        :return: boolean
        """
        if "OrderID" in data.keys() and "ContactEmail" in data.keys():
            return True
        raise OrderManagementException("Bad label")

    #pylint: disable=too-many-locals
    def send_product ( self, input_file ):
        """Sends the order included in the input_file"""
        #We create the objects ShipmentsJSONStore
        shipping_json_store=ShipmentsJSONStore()

        #We validate if the input_file is valid
        shipping_json_store.load_input_file(input_file)

        #We save into the variable data the data list
        # that was extracted from the previous load
        data=shipping_json_store.data_list

        #We validate that the keys on data are valid
        self.validate_label(data)

        #check all the informationand create an object from OrderShipping into my_sign
        order = OrderRequest.get_order_by_order_id(data["OrderID"])
        my_sign = OrderShipping(product_id=order.product_id,
                                order_id=data["OrderID"],
                                order_type=order.order_type,
                                delivery_email=data["ContactEmail"])

        #We load and save the new information on shipments_store.json
        shipping_json_store.add(my_sign)

        #We return the tracking code "generated" from my_sign
        return my_sign.tracking_code

    def deliver_product( self, tracking_code ):
        """Register the delivery of the product"""
        # first define the JSONStore class for delivery and shipment
        shipping_json_store=ShipmentsJSONStore()
        deliver_json_store=DeliverJSONStore()

        #We check if the tracking code is valid
        tracking_code=TrackingCode(tracking_code).value

        #search this tracking_code and obtain its time_stamp
        item=shipping_json_store.find("_OrderShipping__tracking_code",tracking_code)
        del_timestamp = item["_OrderShipping__delivery_day"]

        #Check if today is the delivery date
        today= datetime.today().date()
        delivery_date= datetime.fromtimestamp(del_timestamp).date()
        #If today is not the delivery date then we raise an exception
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

        #We open and save to the delivery json
        deliver_json_store.add(tracking_code)

        #If everything is fine and is the delivery date we return True
        return True
