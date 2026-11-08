from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    def get_product_id(self):
        return self._product_id

    def update_stock(self, quantity):
        self._stock = quantity
        return None

    def display_information(self):
        return f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}"

    def to_dict(self):
        return {"id": self._product_id, "name": self._name, "price": self._price, "stock": self._stock}

    @abstractmethod
    def get_fulfilment_info(self):
        """Gets fulfilment info"""
        pass
