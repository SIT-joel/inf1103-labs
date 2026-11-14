from models.product import Product

class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = [] # the list of Product objects

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        return None

    def remove_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                self.__products.remove(product)
                return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        table = ""
        for product in self.__products:
            table += product.display_information() + "\n"
        print(f"""Current Inventory
------------------------------------------------
{table}------------------------------------------------""")
        return None

    def to_list(self) -> list[dict]:
        products = []
        for product in self.__products:
            products.append(product.to_dict())
        return products
