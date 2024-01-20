import pytest

from app.product import Product


class TestProductClass:
    @pytest.mark.parametrize(
        "sku, name, price",
        [
            ("ABC123", "Sample Product", 19),
            ("DEF456", "Another Product", 29.99),
        ],
    )
    def test_product_initialization(self, sku, name, price):
        product = Product(sku, name, price)

        assert product.sku == sku
        assert product.name == name
        assert product.price == price
