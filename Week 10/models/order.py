from models.order_line import OrderLine
from models.product import Product

class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        # Composition: the Order creates and manages its own OrderLine objects.
        # An OrderLine belongs to exactly one Order and is never transferred.
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The OrderLine is created inside the Order (composition), never passed in from outside
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)
        return None

    def remove_order_line(self, product_id: str) -> OrderLine | None:
        # Removes and returns the OrderLine for the given product; the Product itself is untouched
        for order_line in self.order_lines:
            if order_line.product.get_product_id() == product_id:
                self.order_lines.remove(order_line)
                return order_line
        return None

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()
        return total
