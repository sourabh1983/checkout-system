from app.pricing_rules import PricingRule
from app.product import Product
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Checkout:
    pricing_rules: Dict[Product, PricingRule]
    products: Dict[Product, int] = field(default_factory=dict)

    def scan(self, product: Product) -> None:
        if self.products.get(product):
            self.products[product] += 1
        else:
            self.products[product] = 1

    def total(self) -> float:
        total_price = 0
        for product, quantity in self.products.items():
            rule = self.pricing_rules.get(product)
            if rule:
                total_price += rule.get_price(product, self.products)
            else:
                total_price += product.price * quantity
        return total_price
