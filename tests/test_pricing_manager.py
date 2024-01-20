from app.pricing_rule_manager import PricingManager
from app.pricing_rules import PricingRule
from app.product import Product


def test_add_pricing_rule():
    manager = PricingManager(pricing_rules={})
    product = Product(sku="a", name="Test Product", price=100)
    rule = PricingRule()

    manager.add_pricing_rule(product, rule)

    assert manager.pricing_rules == {product: rule}


def test_get_pricing_rules():
    manager = PricingManager()
    product1 = Product(sku="a", name="Test Product 1", price=100)
    rule1 = PricingRule()

    product2 = Product(sku="b", name="Test Product 2", price=200)
    rule2 = PricingRule()

    manager.add_pricing_rule(product1, rule1)
    manager.add_pricing_rule(product2, rule2)

    rules = manager.get_pricing_rules()

    assert rules == {product1: rule1, product2: rule2}
