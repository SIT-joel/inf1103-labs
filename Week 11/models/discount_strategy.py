from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        self._percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self._percentage / 100)

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        self._threshold: float = threshold
        self._amount: float = amount

    def apply(self, total: float) -> float:
        return total - self._amount if total >= self._threshold else total

class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95
