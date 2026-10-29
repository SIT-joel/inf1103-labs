import json
import os

from models.product import Product
from models.inventory import Inventory

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
