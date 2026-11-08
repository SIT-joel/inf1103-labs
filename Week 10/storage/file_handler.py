import json
import os

from models.physical_product import PhysicalProduct
from models.digital_product import DigitalProduct
from models.subscription_product import SubscriptionProduct
from models.inventory import Inventory

def load_inventory():
    inventory = Inventory() # begin with an empty inventory
    if os.path.exists("data/inventory.json"):
        print("""inventory.json found.
Inventory loaded successfully.""")
        with open("inventory.json","r") as f:
            products = json.load(f)
        for product in products:
            if product["product_type"] == "physical":
                inventory.add_product(PhysicalProduct(product["id"], product["name"], product["price"], product["stock"], product["weight"]))
            elif product["product_type"] == "digital":
                inventory.add_product(DigitalProduct(product["id"], product["name"], product["price"], product["stock"], product["download_size"]))
            elif product["product_type"] == "subscription product":
                inventory.add_product(SubscriptionProduct(product["id"], product["name"], product["price"], product["stock"], product["duration"]))
    else:
        print("""inventory.json not found.
Starting with an empty inventory.""")
    return inventory

def save_inventory(inventory):
    with open("data/inventory.json","w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    return None
