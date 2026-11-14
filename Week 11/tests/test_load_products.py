from models.inventory import Inventory
from models.supplier import Supplier
from storage.file_handler import load_products

SUPPLIER = Supplier("SUP-001", "TechSupply Co", "sales@techsupply.example")

def test_loads_valid_rows_and_skips_invalid_rows(capsys):
    inventory = Inventory()
    load_products("products.csv", inventory, SUPPLIER)
    output = capsys.readouterr().out
    assert inventory.find_product("P001") != None
    assert inventory.find_product("D001") != None
    assert inventory.find_product("P003") != None
    assert inventory.find_product("S001") is None
    assert inventory.find_product("P002") is None
    assert "Skipping invalid row: Unknown product type: service" in output
    assert "Skipping invalid row: could not convert string to float: 'abc'" in output
    assert "3 products loaded." in output
    assert "Load attempt finished." in output

def test_missing_file_is_handled_gracefully(capsys):
    inventory = Inventory()
    load_products("missing.csv", inventory, SUPPLIER)
    output = capsys.readouterr().out
    assert inventory.find_product("P001") is None
    assert "Products file not found: missing.csv" in output
    assert "Load attempt finished." in output
