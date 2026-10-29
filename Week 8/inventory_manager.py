from models.product import Product
from storage.file_handler import load_inventory, save_inventory

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
            print("\nProduct added successfully!")
        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)
            if product == None:
                print("\nProduct not found.")
            else:
                details = product.to_dict()
                print(f"""
Product Found:
Name: {details['name']}
Current Stock: {details['stock']}
""")
                product.update_stock(get_valid_stock("New Stock Quantity: "))
                print("\nStock updated successfully!")
        elif option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)
            if product == None:
                print("\nProduct not found.")
            else:
                details = product.to_dict()
                print(f"""
Product Found
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
