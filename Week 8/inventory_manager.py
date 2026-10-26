import json
import os

banner = """========================================
INVENTORY MANAGEMENT SYSTEM
========================================
"""

menu = """----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Exit
----------------------------
"""

goodbye = """
Thank you for using Inventory Management System.
Program terminated."""

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

def load_inventory():
    inventory = Inventory() # begin with an empty inventory
    if os.path.exists("inventory.json"):
        print("inventory.json found.")
        with open("inventory.json","r") as f:
            products = json.load(f)
        for product in products:
            inventory.add_product(Product(product["id"], product["name"], product["price"], product["stock"]))
        print("Inventory loaded successfully.")
    else:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
    return inventory

def save_inventory(inventory):
    with open("inventory.json","w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    return None

def get_valid_price():
    while True:
        price_input = input("Price: ")
        try:
            price = float(price_input)
            if price >= 0:
                return price
        except ValueError:
            pass
        print("Error: price must be a number or it must not be a negative number")

def get_valid_stock(prompt):
    while True:
        stock_input = input(prompt)
        if not stock_input.isdigit():
            print("Error: stock quantity must be a number or it must not be a negative number")
            continue
        return int(stock_input)

def main():
    print(banner)
    inventory = load_inventory()
    print()
    print(menu)
    while True:
        option = input("Enter option: ")
        print()
        if option == "1":
            inventory.display_all()
        elif option == "2":
            print("Add New Product")
            while True:
                product_id = input("Product ID: ")
                if len(product_id) == 0:
                    print("Invalid Product ID!")
                    continue
                if inventory.search_product(product_id) != None:
                    print("Error: product ID already exists")
                    continue
                break
            while True:
                name = input("Product Name: ")
                if len(name) != 0:
                    break
                print("Invalid Product Name!")
            price = get_valid_price()
            stock = get_valid_stock("Stock Quantity: ")
            product = Product(product_id, name, price, stock) # create the Product object from the Product class
            inventory.add_product(product)
            print()
            print("Product added successfully!")
        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")
            print()
            product = inventory.search_product(product_id)
            if product == None:
                print("Product not found.")
            else:
                details = product.to_dict()
                print("Product Found:")
                print(f"Name: {details['name']}")
                print(f"Current Stock: {details['stock']}")
                print()
                product.update_stock(get_valid_stock("New Stock Quantity: "))
                print()
                print("Stock updated successfully!")
        elif option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ")
            print()
            product = inventory.search_product(product_id)
            if product == None:
                print("Product not found.")
            else:
                details = product.to_dict()
                print(f"""Product Found
------------------------------------------------
ID: {details['id']}
Name: {details['name']}
Price: ${details['price']:.2f}
Stock: {details['stock']}
------------------------------------------------""")
        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif option == "6": # save before exit
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            break
        else:
            print("Invalid option!")
        print()
    print(goodbye)

main()
