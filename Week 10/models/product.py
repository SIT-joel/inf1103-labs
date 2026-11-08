from abc import ABC, abstractmethod

from models.supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self._product_id: str = product_id
        self._name: str = name
        self._price: float = price
        self._stock: int = stock
        # Association: a Product knows about its Supplier but does not own it.
        # The Supplier is created independently and passed in when the Product is created.
        self.supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self._product_id

    def get_price(self) -> float:
        return self._price

    def update_stock(self, quantity: int) -> None:
        self._stock = quantity
        return None

    def display_information(self) -> str:
        return f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}"

    def to_dict(self) -> dict:
        return {"id": self._product_id, "name": self._name, "price": self._price, "stock": self._stock,
                "supplier": {"supplier_id": self.supplier.supplier_id, "name": self.supplier.name, "contact_email": self.supplier.contact_email}}

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Gets fulfilment info"""
        pass
