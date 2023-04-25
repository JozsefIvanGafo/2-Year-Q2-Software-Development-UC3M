"""File containing test for the singleton"""
from unittest import TestCase
from uc3m_logistics import OrderManager
from uc3m_logistics.storage.deliver_json_store import DeliverJSONStore
from uc3m_logistics.storage.orders_json_store import OrdersJSONStore
from uc3m_logistics.storage.shipping_json_store import ShipmentsJSONStore

class TestSingleton(TestCase):
    """Class contining the singleton test for OrderManager and for JsonFiles classes"""
    def test_singleton_order_manager1(self):
        """Method that test the singleton on Order Manager"""
        om1 = OrderManager()
        om2 = OrderManager()
        om3 = OrderManager()

        self.assertEqual(om1,om2)
        self.assertEqual(om2,om3)
        self.assertEqual(om1,om3)
    def test_singleton_orders_json(self):
        """Method that test the singleton on orders_json_store"""
        oj1 = OrdersJSONStore()
        oj2 = OrdersJSONStore()
        oj3 = OrdersJSONStore()

        self.assertEqual(oj1,oj2)
        self.assertEqual(oj2,oj3)
        self.assertEqual(oj1,oj3)
    def test_singleton_shipments_json(self):
        """Method that test the singleton on shipmentJsonStore"""
        sj1 = ShipmentsJSONStore()
        sj2 = ShipmentsJSONStore()
        sj3 = ShipmentsJSONStore()

        self.assertEqual(sj1,sj2)
        self.assertEqual(sj2,sj3)
        self.assertEqual(sj1,sj3)

    def test_singleton_deliver_json(self):
        """Method that test the singleton on DeliverJsonStore"""
        dj1 = DeliverJSONStore()
        dj2 = DeliverJSONStore()
        dj3 = DeliverJSONStore()

        self.assertEqual(dj1,dj2)
        self.assertEqual(dj2,dj3)
        self.assertEqual(dj1,dj3)

