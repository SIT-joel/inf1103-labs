import pytest

from models.digital_product import DigitalProduct
from models.physical_product import PhysicalProduct
from models.product import Product
from models.product_factory import ProductFactory
from models.subscription_product import SubscriptionProduct
from models.supplier import Supplier

SUPPLIER = Supplier("SUP-001", "TechSupply Co", "sales@techsupply.example")

def test_creates_physical_product() -> None:
    product = ProductFactory.create("physical", "P-100", "Desk Lamp", 25.0, 10, SUPPLIER, 2.5)
    assert isinstance(product, PhysicalProduct)
    assert isinstance(product, Product)
    assert product.calculate_shipping_cost() == 0.25

def test_creates_digital_product() -> None:
    product = ProductFactory.create("digital", "D-100", "Photo Editor", 49.9, 100, SUPPLIER, 250.0)
    assert isinstance(product, DigitalProduct)
    assert isinstance(product, Product)

def test_creates_subscription_product() -> None:
    product = ProductFactory.create("subscription product", "S-100", "Cloud Backup", 4.99, 100, SUPPLIER, 30)
    assert isinstance(product, SubscriptionProduct)
    assert isinstance(product, Product)

def test_unknown_product_type_raises_value_error() -> None:
    with pytest.raises(ValueError) as error:
        ProductFactory.create("service", "S-001", "Installation", 30.0, 5, SUPPLIER, 0.0)
    assert "Unknown product type: service" in str(error.value)
