from models.product import Product

class SubscriptionProduct(Product):

    def __init__(self, product_id, name, price, stock, duration):
        super().__init__(product_id, name, price, stock)
        self._duration = duration

    def display_information(self):
        product_information = super().display_information()
        product_information = f"{product_information} | Subscription Duration: {self._duration} days"
        return product_information


    def get_fulfilment_info(self):
        return "This Product Subscription is delivered digitally"

    def to_dict(self):
        object_json = super().to_dict()
        object_json["product_type"] = "subscription product"
        object_json["duration"] = self._duration
        return object_json