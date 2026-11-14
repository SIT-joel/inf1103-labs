from models.supplier import Supplier
from models.product_factory import ProductFactory
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

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")

def get_valid_stock(prompt: str) -> int:
    while True:
        stock_input = input(prompt)
        if not stock_input.isdigit():
            print("Error: stock quantity must be a number and it must not be a negative number")
            continue
        return int(stock_input)

def get_valid_product_type() -> str:
    while True:
        product_type = input("Product Type (Physical/Digital/Subscription product):").lower()
        if product_type in ["physical","digital", "subscription product"]:
            return product_type
        else:
            print("Error: Invalid product type, product type must be physical, digital or subscription product")

def get_valid_weight() -> float:
    while True:
        weight_input = input("Enter the weight of the product in kilograms:")
        try:
            weight_input = float(weight_input)
            if weight_input <= 0:
              raise ValueError("Error: Weight cannot be negative")
            return weight_input
        except ValueError:
            print("Error: weight must be a integer or float and cannot be less than or equal to 0")

def get_valid_download_size() -> float:
    while True:
        download_size_input = input("Enter the download size of the product in megabytes:")
        try:
            download_size_input = float(download_size_input)
            if download_size_input <= 0:
              raise ValueError("Error: Download Size cannot be negative")
            return download_size_input
        except ValueError:
            print("Error: Download Size must be a integer or float and cannot be less than or equal to 0")

def get_valid_duration() -> int:
    while True:
        duration_input = input("Duration of Subscription in days:")
        if not duration_input.isdigit():
            print("Error: duration must be a number and it must not be a negative number")
            continue
        duration_input = int(duration_input)
        if duration_input <= 0:
            print("Error: duration must be above 0")
            continue
        return int(duration_input)

def get_valid_supplier() -> Supplier:
    # The Supplier is created independently and then supplied to the Product (association)
    print("Supplier Details")
    while True:
        supplier_id = input("Supplier ID: ")
        if len(supplier_id) != 0:
            break
        print("Invalid Supplier ID!")
    while True:
        supplier_name = input("Supplier Name: ")
        if len(supplier_name) != 0:
            break
        print("Invalid Supplier Name!")
    while True:
        contact_email = input("Supplier Contact Email: ")
        if len(contact_email) != 0:
            break
        print("Invalid Supplier Contact Email!")
    return Supplier(supplier_id, supplier_name, contact_email)

def main() -> None:
    print(banner)
    inventory = load_inventory()
    print()
    while True:
        print(menu)
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
                if inventory.find_product(product_id) != None:
                    print("Error: product ID already exists")
                    continue
                break
            while True:
                name = input("Product Name: ")
                if len(name) != 0:
                    break
                print("Invalid Product Name!")
            price = get_positive_float("Price: ")
            stock = get_valid_stock("Stock Quantity: ")
            supplier = get_valid_supplier()
            product_type = get_valid_product_type()
            extra = 0.0
            if product_type == "physical":
                extra = get_valid_weight()
            elif product_type == "digital":
                extra = get_valid_download_size()
            elif product_type == "subscription product":
                extra = get_valid_duration()
            product = ProductFactory.create(product_type, product_id, name, price, stock, supplier, extra)
            if product_type == "physical":
                print(f"Shipping cost for 1 unit of this product is {product.calculate_shipping_cost():.2f}")
            print(product.get_fulfilment_info()) # This prints out if the product requires physical or digital delivery
            inventory.add_product(product)
            print("\nProduct added successfully!")
        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")
            product = inventory.find_product(product_id)
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
            product = inventory.find_product(product_id)
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
