from dataclasses import dataclass, field
from typing import Dict

from app.pricing_rules import PricingRule
from app.product import Product


@dataclass
class PricingManager:
    pricing_rules: Dict[Product, PricingRule] = field(default_factory=dict)

    def add_pricing_rule(self, product: Product, pricing_rule: PricingRule):
        self.pricing_rules[product] = pricing_rule

    def get_pricing_rules(self) -> dict:
        return self.pricing_rules
