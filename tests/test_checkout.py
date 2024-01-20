from app.checkout import Checkout
from app.pricing_rule_manager import PricingManager
from app.pricing_rules import XForYRule, BulkDiscountRule, FreeProductBundleRule
from app.product import Product


def test_checkout():
    pricing_manager = PricingManager()

    # Creating instances of the Product class
    ipad = Product("ipd", "Super iPad", 550)
    macbook_pro = Product("mbp", "MacBook Pro", 1000)
    apple_tv = Product("atv", "Apple TV", 100)
    vga = Product("vga", "VGA adapter", 30.00)

    # Adding pricing rules to the manager
    pricing_manager.add_pricing_rule(apple_tv, XForYRule(x_quantity=3, y_quantity=2))
    pricing_manager.add_pricing_rule(
        ipad, BulkDiscountRule(discount_threshold=4, discount_price=500)
    )
    pricing_manager.add_pricing_rule(
        vga, FreeProductBundleRule(main_product=macbook_pro)
    )

    co = Checkout(pricing_rules=pricing_manager.get_pricing_rules())

    # Add items to the checkout
    # 5 ipad, discounted price of 500, $2500
    co.scan(ipad)
    co.scan(ipad)
    co.scan(ipad)
    co.scan(ipad)
    co.scan(ipad)
    # 3 apple tv, buy 3 pay 2, $200
    co.scan(apple_tv)
    co.scan(apple_tv)
    co.scan(apple_tv)
    # 3 macbook pro, $3000
    co.scan(macbook_pro)
    co.scan(macbook_pro)
    co.scan(macbook_pro)
    # 5 vga adaptor, 3 free with macbook, 2 extra = $60
    co.scan(vga)
    co.scan(vga)
    co.scan(vga)
    co.scan(vga)
    co.scan(vga)

    # Total 2500 + 200 + 3000 + 60 = 5760.0
    assert co.total() == 5760.0
