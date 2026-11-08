"""Lab 8 (Week 10) test evidence.

Covers the lab's testing requirements:
- Section 2: Supplier/Product association (including the "Predict first" del supplier check)
- Section 3: Inventory/Product aggregation (remove from one inventory, add to another)
- Section 4: Order/OrderLine composition (including the "Predict first" object-count check)
- Section 6: LSP substitutability via show_product_details(product: Product)
- Section 7: Polymorphism through the common Product abstraction (no isinstance)
- Section 5: type-hint evidence dump (method signatures)

Run from this folder:  python test_relationships.py
"""

import inspect

from models.digital_product import DigitalProduct
from models.inventory import Inventory
from models.order import Order
from models.order_line import OrderLine
from models.physical_product import PhysicalProduct
from models.product import Product
from models.subscription_product import SubscriptionProduct
from models.supplier import Supplier

PASSED = 0
FAILED = 0


def check(label: str, condition: bool) -> None:
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  PASS: {label}")
    else:
        FAILED += 1
        print(f"  FAIL: {label}")


def show_product_details(product: Product) -> None:
    # Section 6.2: accepts any Product and only uses behaviour every Product supports
    product.display_information()
    print(f"  fulfilment: {product.get_fulfilment_info()}")


def test_association() -> None:
    print("=" * 60)
    print("SECTION 2 - ASSOCIATION: Supplier and Product")
    print("=" * 60)

    # Create a Supplier object independently
    supplier = Supplier("SUP-001", "TechSupply Co", "sales@techsupply.example")

    # Create a PhysicalProduct and a DigitalProduct using that Supplier
    physical = PhysicalProduct("P-100", "USB Cable", 5.50, 100, supplier, 0.2)
    digital = DigitalProduct("D-200", "Antivirus 1 Year", 39.99, 500, supplier, 250.0)

    # Display the supplier information through each Product
    print("\nSupplier info through PhysicalProduct:")
    print(f"  {physical.supplier.display_information()}")
    print("Supplier info through DigitalProduct:")
    print(f"  {digital.supplier.display_information()}")

    # Predict first (2.2): what happens if we delete the supplier variable?
    # Each Product stored its own reference to the Supplier object, so the
    # Supplier should still be reachable through both products.
    print("\nPredict first check: del supplier")
    del supplier
    print(f"  {physical.supplier.display_information()}")
    check("Product still displays supplier info after 'del supplier'",
          physical.supplier.display_information() == "Supplier ID: SUP-001 | Name: TechSupply Co | Contact Email: sales@techsupply.example")
    check("DigitalProduct still displays supplier info after 'del supplier'",
          digital.supplier.name == "TechSupply Co")

    # Confirm the Supplier and Products are separate objects that can exist independently
    print("\nObject identity:")
    print(f"  id(Supplier via product) = {id(physical.supplier)}")
    print(f"  id(PhysicalProduct)      = {id(physical)}")
    print(f"  id(DigitalProduct)       = {id(digital)}")
    check("Both products reference the same Supplier object",
          physical.supplier is digital.supplier)
    check("Supplier and Products are separate objects",
          physical is not physical.supplier and digital is not physical.supplier)


def test_aggregation() -> None:
    print()
    print("=" * 60)
    print("SECTION 3 - AGGREGATION: Inventory and Product")
    print("=" * 60)

    # Predict first (3.2): after removal from Inventory A the Product should still
    # work, because the Inventory only held a reference to it.
    supplier = Supplier("SUP-002", "GadgetWorld", "orders@gadgetworld.example")
    # Create the Product BEFORE creating/adding it to an Inventory
    product = PhysicalProduct("P-300", "Keyboard", 25.00, 40, supplier, 0.8)

    inventory_a = Inventory()
    inventory_b = Inventory()

    # Add the Product to Inventory A
    inventory_a.add_product(product)
    check("Product found in Inventory A", inventory_a.find_product("P-300") is product)

    # Remove it from Inventory A and confirm the Product object can still be used
    removed = inventory_a.remove_product("P-300")
    check("remove_product returns the removed Product reference", removed is product)
    check("Product no longer in Inventory A", inventory_a.find_product("P-300") is None)

    print("\nProduct still usable after removal from Inventory A:")
    print(f"  {product.display_information()}")
    product.update_stock(35)  # a normal Product operation still works
    check("Product still usable (update_stock) after removal", product.to_dict()["stock"] == 35)

    # Add the same Product object to Inventory B
    inventory_b.add_product(product)
    check("Same Product object added to Inventory B", inventory_b.find_product("P-300") is product)
    print("\nRemoving the Product from an inventory does not destroy the Product itself.")


def test_composition() -> None:
    print()
    print("=" * 60)
    print("SECTION 4 - COMPOSITION: Order and OrderLine")
    print("=" * 60)

    supplier = Supplier("SUP-003", "OfficeHub", "hello@officehub.example")
    mouse = PhysicalProduct("P-400", "Mouse", 12.50, 80, supplier, 0.15)
    license_key = DigitalProduct("D-401", "Office Suite Key", 89.00, 999, supplier, 3.5)

    # Create an Order and add two products through add_order_line()
    order = Order("ORD-001")
    order.add_order_line(mouse, 2)          # Order creates its own OrderLine
    order.add_order_line(license_key, 1)

    print("\nOrder lines (each created by the Order itself):")
    for line in order.order_lines:
        print(f"  {line.product.display_information()} | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
    total = order.calculate_total()
    print(f"Order total: ${total:.2f}")
    check("calculate_total sums the OrderLine subtotals", total == (12.50 * 2) + (89.00 * 1))
    check("Order created and manages its own OrderLine objects",
          len(order.order_lines) == 2 and all(isinstance(line, OrderLine) for line in order.order_lines))

    # Predict first (4.3): add the same Product to a different Order.
    # Expect: one extra OrderLine per Order, but still only 1 Product object.
    order2 = Order("ORD-002")
    order2.add_order_line(mouse, 3)
    print("\nPredict first check: same Product in two Orders")
    print(f"  id(mouse)           = {id(mouse)}")
    print(f"  id(line in ORD-001) = {id(order.order_lines[0].product)}")
    print(f"  id(line in ORD-002) = {id(order2.order_lines[0].product)}")
    mouse_lines = [line for line in order.order_lines + order2.order_lines if line.product is mouse]
    distinct_products = len({id(line.product) for line in mouse_lines})
    check(f"Two OrderLines share exactly one Product object (lines={len(mouse_lines)}, products={distinct_products})",
          len(mouse_lines) == 2 and distinct_products == 1)
    check("Each Order created its own OrderLine",
          order.order_lines[0] is not order2.order_lines[0])

    # Remove an order line through an Order method
    removed_line = order.remove_order_line("P-400")
    check("Order removed its own OrderLine", removed_line is not None and len(order.order_lines) == 1)
    check("Removed OrderLine no longer part of the Order",
          all(line.product.get_product_id() != "P-400" for line in order.order_lines))
    check("The Product itself is untouched by removing the OrderLine", mouse.to_dict()["stock"] == 80)
    print("\nAn OrderLine belongs to exactly one Order and is never transferred between Orders.")


def test_lsp() -> None:
    print()
    print("=" * 60)
    print("SECTION 6 - LISKOV SUBSTITUTION PRINCIPLE")
    print("=" * 60)

    supplier = Supplier("SUP-004", "ByteBarn", "support@bytebarn.example")
    physical = PhysicalProduct("P-500", "HDMI Cable", 8.00, 60, supplier, 0.3)
    digital = DigitalProduct("D-501", "Ebook", 15.00, 1000, supplier, 12.0)
    subscription = SubscriptionProduct("S-502", "Cloud Backup 30d", 4.99, 100, supplier, 30)

    # show_product_details(product: Product) works for every subclass without modification
    print("\nshow_product_details with a PhysicalProduct:")
    show_product_details(physical)
    print("show_product_details with a DigitalProduct:")
    show_product_details(digital)
    print("show_product_details with a SubscriptionProduct:")
    show_product_details(subscription)

    # Both product types can be added to an Inventory and used by its normal operations
    inventory = Inventory()
    inventory.add_product(physical)
    inventory.add_product(digital)
    inventory.add_product(subscription)
    check("Inventory holds all product types through the Product abstraction",
          inventory.find_product("P-500") is physical and inventory.find_product("D-501") is digital
          and inventory.find_product("S-502") is subscription)
    found = inventory.find_product("D-501")
    found.update_stock(950)  # normal Product operation through the base type
    check("Normal Product operations work on any subclass through the Inventory", digital.to_dict()["stock"] == 950)

    # 6.3: an expectation of the parent class preserved by the subclasses:
    # update_stock(quantity) replaces the stored stock, and to_dict() reflects it.
    physical.update_stock(55)
    digital.update_stock(900)
    check("update_stock keeps its expected meaning for PhysicalProduct", physical.to_dict()["stock"] == 55)
    check("update_stock keeps its expected meaning for DigitalProduct", digital.to_dict()["stock"] == 900)


def test_polymorphism() -> None:
    print()
    print("=" * 60)
    print("SECTION 7 - POLYMORPHISM THROUGH THE PRODUCT ABSTRACTION")
    print("=" * 60)

    supplier = Supplier("SUP-005", "PixelPress", "team@pixelpress.example")
    inventory = Inventory()
    products: list[Product] = [
        PhysicalProduct("P-600", "Webcam", 45.00, 25, supplier, 0.4),
        DigitalProduct("D-601", "Photo Filter Pack", 9.99, 500, supplier, 80.0),
        SubscriptionProduct("S-602", "Stock Photos 90d", 19.99, 200, supplier, 90),
    ]
    for product in products:
        inventory.add_product(product)

    # Predict first (7.2): each product prints its own specialised fulfilment info.
    # One loop through the common Product type - no separate loops, no isinstance.
    print("\nPredict first check: one loop, common Product type, no isinstance:")
    for product in products:  # the same objects the Inventory aggregates
        product.display_information()
        print(f"  -> {product.get_fulfilment_info()}")
    print()
    inventory.display_all()

    fulfilment_messages = [product.get_fulfilment_info() for product in products]
    check("Each subclass produced its own specialised output", len(set(fulfilment_messages)) == 3)
    check("Mixed inventory loop used only behaviour declared on Product",
          all(callable(getattr(p, "display_information")) and callable(getattr(p, "get_fulfilment_info")) for p in products))


def format_annotation(annotation) -> str:
    import types as types_module
    if annotation is inspect.Parameter.empty or annotation is inspect.Signature.empty:
        return "?"
    if isinstance(annotation, type):
        return "None" if annotation is type(None) else annotation.__name__
    if isinstance(annotation, types_module.UnionType):
        return " | ".join(format_annotation(arg) for arg in annotation.__args__)
    return str(annotation)


def type_hint_evidence() -> None:
    print()
    print("=" * 60)
    print("SECTION 5 - TYPE HINT EVIDENCE (method signatures)")
    print("=" * 60)
    samples = [
        ("Product.__init__", Product.__init__),
        ("Product.update_stock", Product.update_stock),
        ("Product.get_fulfilment_info", Product.get_fulfilment_info),
        ("Supplier.display_information", Supplier.display_information),
        ("Inventory.add_product", Inventory.add_product),
        ("Inventory.remove_product", Inventory.remove_product),
        ("Inventory.find_product", Inventory.find_product),
        ("Order.add_order_line", Order.add_order_line),
        ("Order.calculate_total", Order.calculate_total),
        ("OrderLine.calculate_subtotal", OrderLine.calculate_subtotal),
    ]
    for name, func in samples:
        sig = inspect.signature(func)
        params = ", ".join(f"{p.name}: {format_annotation(p.annotation)}"
                           for p in sig.parameters.values() if p.name != "self")
        print(f"  {name}({params}) -> {format_annotation(sig.return_annotation)}")


def main() -> None:
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()
    type_hint_evidence()

    print()
    print("=" * 60)
    print(f"RESULT: {PASSED} passed, {FAILED} failed")
    print("=" * 60)
    if FAILED > 0:
        raise SystemExit(1)


main()
