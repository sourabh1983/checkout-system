import pytest

from app.pricing_rules import XForYRule, BulkDiscountRule, FreeProductBundleRule
from app.product import Product


@pytest.mark.parametrize(
    "x_quantity, y_quantity, purchase_qty, expected_price",
    [
        (3, 2, 2, 200.0),
        (3, 2, 6, 400.0),
        (3, 2, 10, 700.0),
        (4, 2, 10, 600.0),
        (4, 2, 4, 200.0),
        (2, 4, 2, 400.0),
    ],
)
def test_x_for_y_rule(x_quantity, y_quantity, purchase_qty, expected_price):
    product = Product("atv", "Apple TV", 100.0)
    co_products = {product: purchase_qty}
    rule = XForYRule(x_quantity=x_quantity, y_quantity=y_quantity)

    price = rule.get_price(product, co_products)

    assert price == expected_price


@pytest.mark.parametrize(
    "discount_threshold, discount_price, purchase_qty, expected_price",
    [
        (3, 150, 4, 600.0),
        (4, 150, 4, 800.0),
        (0, 150, 1, 150.0),
        (5, 150, 4, 800.0),
    ],
)
def test_bulk_discount_rule(
    discount_threshold, discount_price, purchase_qty, expected_price
):
    product = Product("atv", "Apple TV", 200.0)
    co_products = {product: purchase_qty}
    rule = BulkDiscountRule(
        discount_threshold=discount_threshold, discount_price=discount_price
    )

    price = rule.get_price(product, co_products)

    assert price == expected_price


@pytest.mark.parametrize(
    "main_product_qty, free_product_qty, free_product_expected_price",
    [
        (3, 3, 0.0),
        (3, 2, 0.0),
        (3, 4, 30.0),
        (6, 4, 0.0),
    ],
)
def test_free_product_bundle_rule(
    main_product_qty, free_product_qty, free_product_expected_price
):
    main_product = Product("mbp", "MAC Book Pro", 1000.0)
    free_product = Product("vga", "VGA Adaptor", 30.0)
    co_products = {free_product: free_product_qty, main_product: main_product_qty}
    rule = FreeProductBundleRule(main_product=main_product)

    price = rule.get_price(free_product=free_product, co_products=co_products)

    assert price == free_product_expected_price
