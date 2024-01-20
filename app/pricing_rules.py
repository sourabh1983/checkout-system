from dataclasses import dataclass
from typing import Dict

from app.product import Product


@dataclass
class PricingRule:
    """
    Base class for pricing rules
    """

    def get_price(self, item, co_products: Dict[Product, int]) -> float:
        raise NotImplementedError("Subclasses must implement this method")


@dataclass
class XForYRule(PricingRule):
    """
    We're going to have a 3(x quantity) for 2(y quantity) deal on Apple TVs.
    For example, if you buy 3 Apple TVs, you will pay the price of 2 only
    """

    x_quantity: int
    y_quantity: int

    def get_price(self, product: Product, co_products: Dict[Product, int]) -> float:
        total_quantity = co_products.get(product, 0)

        deal_count, remaining_quantity = divmod(total_quantity, self.x_quantity)

        discounted_price_groups = deal_count * (product.price * self.y_quantity)
        remaining_price = remaining_quantity * product.price

        return discounted_price_groups + remaining_price if total_quantity > 0 else 0.0


@dataclass
class BulkDiscountRule(PricingRule):
    """
    Example, New Super iPad will have a bulk discounted applied, where the price
    will drop to $499.99 each, if someone buys more than 4
    """

    discount_threshold: int
    discount_price: float

    def get_price(self, product: Product, co_products: Dict[Product, int]) -> float:
        quantity = co_products.get(product, 0)

        return (
            quantity * self.discount_price
            if quantity > self.discount_threshold
            else quantity * product.price
        )


@dataclass
class FreeProductBundleRule(PricingRule):
    """
    Example, bundle in a free VGA adapter free of charge with every MacBook Pro sold
    """

    main_product: Product

    def get_price(
        self, free_product: Product, co_products: Dict[Product, int]
    ) -> float:
        main_product_qty = co_products.get(self.main_product, 0)
        free_product_qty = co_products.get(free_product, 0)

        if free_product_qty > main_product_qty:
            return (free_product_qty - main_product_qty) * free_product.price

        return 0.0
