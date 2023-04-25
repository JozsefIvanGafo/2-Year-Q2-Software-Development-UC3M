"""Module """
import datetime
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
    class __OrderManager():
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments
        def register_order( self, product_id,
                            order_type,
                            address,
                            phone_number,
                            zip_code ):
            """Method that registers and order and verifies its parameters"""
            #We define an object of OrdersJSONStore
            #orders_json_store = OrdersJSONStore()

            #We validate and we create an object of OrderRequest
            #if self.validate_ean13(product_id):
            my_order = OrderRequest(product_id,
                                        order_type,
                                        address,
                                        phone_number,
                                        zip_code)

            #Load and store the information of my_order into orders_store.json
            my_order.save()
            #orders_json_store.add(my_order)
            #we return my order id of the product
            return my_order.order_id

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
            #self.validate_label(data)

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

    instance = None

    def __new__(cls):
        if not OrderManager.instance:
            OrderManager.instance = OrderManager.__OrderManager()
        return OrderManager.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
