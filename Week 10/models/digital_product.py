from models.product import Product
from models.supplier import Supplier

class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = download_size

    def display_information(self) -> str:
        product_information = super().display_information()
        product_information = f"{product_information} | Download Size: {self._download_size} mb"
        return product_information

    def get_fulfilment_info(self) -> str:
        return "This Product is delivered digitally"

    def to_dict(self) -> dict:
        object_json = super().to_dict()
        object_json["product_type"] = "digital"
        object_json["download_size"] = self._download_size
        return object_json
