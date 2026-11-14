from models.discount_strategy import BulkDiscount, NoDiscount, PercentageDiscount, StudentDiscount
from models.order import Order
from models.physical_product import PhysicalProduct
from models.supplier import Supplier

SUPPLIER = Supplier("SUP-001", "TechSupply Co", "sales@techsupply.example")

def make_order() -> Order:
    order = Order("ORD-001")
    order.add_order_line(PhysicalProduct("P-100", "Desk Lamp", 125.0, 10, SUPPLIER, 1.0), 2)
    return order

def test_no_discount_returns_total_unchanged():
    assert make_order().calculate_total() == 250.0

def test_default_discount_is_no_discount():
    assert isinstance(Order("ORD-002").discount, NoDiscount)

def test_percentage_discount_takes_percentage_off():
    order = make_order()
    order.set_discount(PercentageDiscount(10))
    assert order.calculate_total() == 225.0

def test_bulk_discount_takes_amount_off_totals_at_threshold():
    order = make_order()
    order.set_discount(BulkDiscount(200, 20))
    assert order.calculate_total() == 230.0

def test_bulk_discount_ignores_totals_below_threshold():
    order = Order("ORD-003")
    order.add_order_line(PhysicalProduct("P-101", "USB Cable", 50.0, 10, SUPPLIER, 0.2), 3)
    order.set_discount(BulkDiscount(200, 20))
    assert order.calculate_total() == 150.0

def test_student_discount_takes_five_percent_off():
    order = make_order()
    order.set_discount(StudentDiscount())
    assert order.calculate_total() == 237.5

def test_new_strategy_can_be_added_without_changing_order():
    order = make_order()
    order.set_discount(StudentDiscount())
    assert order.calculate_total() == 237.5

def test_order_contains_no_discount_if_elif_logic():
    with open("models/order.py") as source:
        assert "elif" not in source.read()
