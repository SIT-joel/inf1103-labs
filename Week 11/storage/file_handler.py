import csv
import json
import os

from models.product_factory import ProductFactory
from models.supplier import Supplier
from models.inventory import Inventory

def load_inventory() -> Inventory:
    inventory = Inventory() # begin with an empty inventory
    if os.path.exists("data/inventory.json"):
        print("""inventory.json found.
Inventory loaded successfully.""")
        with open("data/inventory.json","r") as f:
            products = json.load(f)
        for product in products:
            supplier = Supplier(product["supplier"]["supplier_id"], product["supplier"]["name"], product["supplier"]["contact_email"])
            extra = 0.0
            if product["product_type"] == "physical":
                extra = product["weight"]
            elif product["product_type"] == "digital":
                extra = product["download_size"]
            elif product["product_type"] == "subscription product":
                extra = product["duration"]
            inventory.add_product(ProductFactory.create(product["product_type"], product["id"], product["name"], product["price"], product["stock"], supplier, extra))
    else:
        print("""inventory.json not found.
Starting with an empty inventory.""")
    return inventory

def save_inventory(inventory: Inventory) -> None:
    with open("data/inventory.json","w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    return None

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            rows = csv.reader(file)
            next(rows) # skip the header row
            loaded = 0
            for row in rows:
                try:
                    product = ProductFactory.create(row[0], row[1], row[2], float(row[3]), int(row[4]), supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping invalid row: {error}")
            print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
