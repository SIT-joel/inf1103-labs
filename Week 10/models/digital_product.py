from models.product import Product

class DigitalProduct(Product):
    
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    def display_information(self):
        product_information = super().display_information()
        product_information = f"{product_information} | Download Size: {self._download_size} mb"
        return product_information

    def get_fulfilment_info(self):
        return "This Product is delivered digitally"

    def to_dict(self):
        object_json = super().to_dict()
        object_json["product_type"] = "digital"
        object_json["download_size"] = self._download_size
        return object_json