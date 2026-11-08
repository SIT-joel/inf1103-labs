from models.product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        # Association: the OrderLine refers to a Product but does not own it.
        # The Product can exist independently and may also be present in an Inventory.
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity
