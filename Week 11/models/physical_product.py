from models.product import Product
from models.canbeshipped import CanBeShipped
from models.supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = weight

    def display_information(self) -> str:
        product_information = super().display_information()
        product_information = f"{product_information} | Weight: {self._weight} kg"
        return product_information

    def get_fulfilment_info(self) -> str:
        return "This Product requires physical shipping"

    def calculate_shipping_cost(self) -> float:
        # Shippings costs is weight in kilograms multipled by $0.1 per kilogram shipping fee
        shipping_costs = self._weight * 0.1
        return shipping_costs

    def to_dict(self) -> dict:
        object_json = super().to_dict()
        object_json["product_type"] = "physical"
        object_json["weight"] = self._weight
        return object_json
