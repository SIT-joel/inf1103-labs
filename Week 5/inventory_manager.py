def display_all(inventory):
    print("Current Inventory")
    print("------------------------------------------------")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("------------------------------------------------")

def add_product(inventory):
    print("Add New Product")
    product_id = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    product = {"id": product_id, "name": name, "price": price, "stock": stock} # each product is a dictionary
    inventory.append(product)
    print()
    print("Product added successfully!")
    return inventory

def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ")
    print()
    for product in inventory:
        if product["id"] == product_id:
            print("Product Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")
            print()
            product["stock"] = int(input("New Stock Quantity: "))
            print()
            print("Stock updated successfully!")
            return inventory
    print("Product not found.")
    return inventory

def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")
    print()
    for product in inventory:
        if product["id"] == product_id:
            print("Product Found")
            print("------------------------------------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("------------------------------------------------")
            return None
    print("Product not found.")
    return None

def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    print()
    inventory = [] # begin with an empty inventory
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Exit")
    print("----------------------------")
    print()
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
            break
        else:
            print("Invalid option!")
        print()
    print()
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")

main()
