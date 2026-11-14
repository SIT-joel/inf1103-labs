from models.discount_strategy import DiscountStrategy, NoDiscount
from models.order_line import OrderLine
from models.product import Product

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)
        return None

    def remove_order_line(self, product_id: str) -> OrderLine | None:
        for order_line in self.order_lines:
            if order_line.product.get_product_id() == product_id:
                self.order_lines.remove(order_line)
                return order_line
        return None

    def set_discount(self, strategy: DiscountStrategy) -> None:
        self.discount = strategy
        return None

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()
        return self.discount.apply(total)
