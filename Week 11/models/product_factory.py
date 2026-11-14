from models.digital_product import DigitalProduct
from models.physical_product import PhysicalProduct
from models.product import Product
from models.subscription_product import SubscriptionProduct
from models.supplier import Supplier

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float, stock: int, supplier: Supplier, extra: float = 0.0) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, extra)
        elif product_type == "subscription product":
            return SubscriptionProduct(product_id, name, price, stock, supplier, int(extra))
        else:
            raise ValueError(f"Unknown product type: {product_type}")
