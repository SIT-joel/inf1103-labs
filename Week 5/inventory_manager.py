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

def load_inventory():
    inventory = [] # begin with an empty inventory
    if os.path.exists("inventory.json"):
        print("inventory.json found.")
        with open("inventory.json","r") as f:
            inventory = json.load(f)
        print("Inventory loaded successfully.")
    else:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
    return inventory

def find_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None

def display_all(inventory):
    print("Current Inventory")
    print("------------------------------------------------")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("------------------------------------------------")

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

def add_product(inventory):
    print("Add New Product")
    while True:
        product_id = input("Product ID: ")
        if len(product_id) == 0:
            print("Invalid Product ID!")
            continue
        if find_product(inventory, product_id) != None:
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
    product = {"id": product_id, "name": name, "price": price, "stock": stock} # each product is a dictionary
    inventory.append(product)
    print()
    print("Product added successfully!")
    return inventory

def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ")
    print()
    product = find_product(inventory, product_id)
    if product == None:
        print("Product not found.")
        return inventory
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    print()
    product["stock"] = get_valid_stock("New Stock Quantity: ")
    print()
    print("Stock updated successfully!")
    return inventory

def product_details(product):
    return f"""Product Found
------------------------------------------------
ID: {product['id']}
Name: {product['name']}
Price: ${product['price']:.2f}
Stock: {product['stock']}
------------------------------------------------"""

def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")
    print()
    product = find_product(inventory, product_id)
    if product == None:
        print("Product not found.")
        return None
    print(product_details(product))
    return None

def save_inventory(inventory):
    with open("inventory.json","w") as f:
        json.dump(inventory, f, indent=4)
    return None

def main():
    print(banner)
    inventory = load_inventory()
    print()
    print(menu)
    while True:
        option = input("Enter option: ")
        print()
        if option == "1":
            display_all(inventory)
        elif option == "2":
            inventory = add_product(inventory)
        elif option == "3":
            inventory = update_stock(inventory)
        elif option == "4":
            search_product(inventory)
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
