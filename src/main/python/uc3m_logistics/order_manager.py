"""Module """
from .order_request import OrderRequest
from .order_shipping import OrderShipping
from .storage.shipping_json_store import ShipmentsJSONStore
from .storage.deliver_json_store import DeliverJSONStore
from .order_delivered import OrderDelivered

class OrderManager:
    """Class for providing the methods for managing the orders process"""

    # pylint: disable=invalid-name
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

            #We validate and we create an object of OrderRequest
            my_order = OrderRequest(product_id,
                                        order_type,
                                        address,
                                        phone_number,
                                        zip_code)

            #Load and store the information of my_order into orders_store.json
            my_order.save()
            return my_order.order_id

        #pylint: disable=too-many-locals
        def send_product ( self, input_file ):
            """Sends the order included in the input_file"""

            my_sign = OrderShipping.get_order_shipping(input_file)
            shipping_json_store = ShipmentsJSONStore()
            shipping_json_store.add(my_sign)

            #We return the tracking code "generated" from my_sign
            return my_sign.tracking_code

        def deliver_product( self, tracking_code ):
            """Register the delivery of the product"""

            order_delivered = OrderDelivered(tracking_code)
            orders_delivered_store = DeliverJSONStore()
            orders_delivered_store.add(order_delivered)
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
