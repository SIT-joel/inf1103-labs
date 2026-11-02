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
        table = ""
        for product in self.__products:
            table += product.display_information() + "\n"
        print(f"""Current Inventory
------------------------------------------------
{table}------------------------------------------------""")
        return None

    def to_list(self):
        products = []
        for product in self.__products:
            products.append(product.to_dict())
        return products
