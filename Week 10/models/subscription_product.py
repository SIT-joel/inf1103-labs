from models.product import Product
from models.supplier import Supplier

class SubscriptionProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, duration: int) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._duration: int = duration

    def display_information(self) -> str:
        product_information = super().display_information()
        product_information = f"{product_information} | Subscription Duration: {self._duration} days"
        return product_information


    def get_fulfilment_info(self) -> str:
        return "This Product Subscription is delivered digitally"

    def to_dict(self) -> dict:
        object_json = super().to_dict()
        object_json["product_type"] = "subscription product"
        object_json["duration"] = self._duration
        return object_json
