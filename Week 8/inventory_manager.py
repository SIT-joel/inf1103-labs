class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id # private attributes, changed only through public methods
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        return self.__product_id

    def update_stock(self, quantity):
        self.__stock = quantity
        return None

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")
        return None

    def to_dict(self):
        return {"id": self.__product_id, "name": self.__name, "price": self.__price, "stock": self.__stock}

class Inventory:
    def __init__(self):
        self.__products = [] # the collection of Product objects

    def add_product(self, product):
        self.__products.append(product)
        return None

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory")
        print("------------------------------------------------")
        for product in self.__products:
            product.display_information()
        print("------------------------------------------------")
        return None

    def to_list(self):
        products = []
        for product in self.__products:
            products.append(product.to_dict())
        return products
