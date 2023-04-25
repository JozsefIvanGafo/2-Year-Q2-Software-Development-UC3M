"""File containing test for the singleton"""
from unittest import TestCase
from uc3m_logistics import OrderManager
from uc3m_logistics.storage.deliver_json_store import DeliverJSONStore
from uc3m_logistics.storage.orders_json_store import OrdersJSONStore
from uc3m_logistics.storage.shipping_json_store import ShipmentsJSONStore

class TestSingleton(TestCase):
    """Class contining the singleton test for OrderManager and for JsonFiles classes"""
    def test_singleton_order_manager1(self):
        """Method that test the singleton on Orer mnger"""
        om1 = OrderManager()
        om2 = OrderManager()
        om3 = OrderManager()

        self.assertEqual(om1,om2)
        self.assertEqual(om2,om3)
        self.assertEqual(om1,om3)
    """def test_singleton_order_manager2(self):
        Method that test the singleton on orders_json_store
        om1 = OrdersJSONStore()
        om2 = OrdersJSONStore()
        om3 = OrdersJSONStore()

        self.assertEqual(om1,om2)
        self.assertEqual(om2,om3)
        self.assertEqual(om1,om3)
    def test_singleton_order_manager3(self):
        Method that test the singleton on shipmentJsonStore
        om1 = ShipmentsJSONStore()
        om2 = ShipmentsJSONStore()
        om3 = ShipmentsJSONStore()

        self.assertEqual(om1,om2)
        self.assertEqual(om2,om3)
        self.assertEqual(om1,om3)"""

