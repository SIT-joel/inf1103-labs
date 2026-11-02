from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        """Implementing classes should have a way to calculates shippping costs"""
        pass