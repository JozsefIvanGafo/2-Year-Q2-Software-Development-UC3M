from .attributes.attribute_tracking_code import TrackingCode
from .storage.shipping_json_store import ShipmentsJSONStore
from .order_management_exception import OrderManagementException
from datetime import datetime
class OrderDelivered():
    def __init__(self,tracking_code):
        self._tracking_code = TrackingCode(tracking_code).value
        self._delivery_day = self.validate_delivery_day()

    def validate_delivery_day(self):
        shipments_store = ShipmentsJSONStore()
        shipment = shipments_store.find("_OrderShipping__tracking_code",self._tracking_code)
        if not shipment:
            raise OrderManagementException("tracking_code is not found")
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(shipment["_OrderShipping__delivery_day"]).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")
        return today.__str__()
