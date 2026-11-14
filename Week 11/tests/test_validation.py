import pytest

from models.order_line import OrderLine
from models.physical_product import PhysicalProduct
from models.supplier import Supplier

SUPPLIER = Supplier("SUP-001", "TechSupply Co", "sales@techsupply.example")

def test_zero_price_rejected():
    with pytest.raises(ValueError):
        PhysicalProduct("P-100", "Desk Lamp", 0, 10, SUPPLIER, 1.0)

def test_negative_price_rejected():
    with pytest.raises(ValueError):
        PhysicalProduct("P-100", "Desk Lamp", -5.0, 10, SUPPLIER, 1.0)

def test_negative_stock_rejected():
    with pytest.raises(ValueError):
        PhysicalProduct("P-100", "Desk Lamp", 25.0, -1, SUPPLIER, 1.0)

def test_zero_stock_is_allowed():
    product = PhysicalProduct("P-100", "Desk Lamp", 25.0, 0, SUPPLIER, 1.0)
    assert product.to_dict()["stock"] == 0

def test_zero_orderline_quantity_rejected():
    product = PhysicalProduct("P-100", "Desk Lamp", 25.0, 10, SUPPLIER, 1.0)
    with pytest.raises(ValueError):
        OrderLine(product, 0)

def test_negative_orderline_quantity_rejected():
    product = PhysicalProduct("P-100", "Desk Lamp", 25.0, 10, SUPPLIER, 1.0)
    with pytest.raises(ValueError):
        OrderLine(product, -2)

def test_valid_values_are_accepted():
    product = PhysicalProduct("P-100", "Desk Lamp", 25.0, 10, SUPPLIER, 1.0)
    line = OrderLine(product, 1)
    assert line.quantity == 1
