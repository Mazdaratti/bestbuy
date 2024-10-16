import unittest
from products import Product
from store import Store


class TestProduct(unittest.TestCase):
    def test_create_product_valid(self):
        product = Product("Test Product", price=100, quantity=10)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 100)
        self.assertEqual(product.quantity, 10)
        self.assertTrue(product.is_active())

    def test_create_product_empty_name(self):
        with self.assertRaises(ValueError):
            Product("", price=100, quantity=10)

    def test_create_product_negative_price(self):
        with self.assertRaises(ValueError):
            Product("Test Product", price=-100, quantity=10)

    def test_create_product_negative_quantity(self):
        with self.assertRaises(ValueError):
            Product("Test Product", price=100, quantity=-10)

    def test_get_quantity(self):
        product = Product("Test Product", price=100, quantity=10)
        self.assertEqual(product.get_quantity(), 10)

    def test_set_quantity_valid(self):
        product = Product("Test Product", price=100, quantity=10)
        product.set_quantity(5)
        self.assertEqual(product.get_quantity(), 5)
        self.assertTrue(product.is_active())

    def test_set_quantity_zero(self):
        product = Product("Test Product", price=100, quantity=10)
        product.set_quantity(0)
        self.assertEqual(product.get_quantity(), 0)
        self.assertFalse(product.is_active())

    def test_set_quantity_negative(self):
        product = Product("Test Product", price=100, quantity=10)
        with self.assertRaises(ValueError):
            product.set_quantity(-5)

    def test_activate_product(self):
        product = Product("Test Product", price=100, quantity=0)
        product.activate()
        self.assertTrue(product.is_active())

    def test_deactivate_product(self):
        product = Product("Test Product", price=100, quantity=0)
        product.deactivate()
        self.assertFalse(product.is_active())

    def test_show_active_product(self):
        product = Product("Test Product", price=100, quantity=10)
        self.assertEqual(product.show(), "Test Product, Price: 100, Quantity: 10")

    def test_show_inactive_product(self):
        product = Product("Test Product", price=100, quantity=2)
        product.set_quantity(0)
        self.assertEqual(product.show(), "Test Product is out of stock.")

    def test_buy_valid_quantity(self):
        product = Product("Test Product", price=100, quantity=10)
        total_cost = product.buy(5)
        self.assertEqual(total_cost, 500)
        self.assertEqual(product.get_quantity(), 5)

    def test_buy_excessive_quantity(self):
        product = Product("Test Product", price=100, quantity=10)
        with self.assertRaises(ValueError):
            product.buy(15)

    def test_buy_inactive_product(self):
        product = Product("Test Product", price=100, quantity=0)
        with self.assertRaises(ValueError):
            product.buy(1)

    def test_buy_negative_quantity(self):
        product = Product("Test Product", price=100, quantity=10)
        with self.assertRaises(ValueError):
            product.buy(-1)

    def test_buy_zero_quantity(self):
        product = Product("Test Product", price=100, quantity=10)
        with self.assertRaises(ValueError):
            product.buy(0)


class TestStore(unittest.TestCase):
    def setUp(self):
        """Set up a store with products for testing."""
        self.product1 = Product("MacBook Air M2", price=1450, quantity=100)
        self.product2 = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
        self.product3 = Product("Google Pixel 7", price=500, quantity=250)
        self.store = Store([self.product1, self.product2, self.product3])

    def test_add_product(self):
        new_product = Product("Test Product", price=100, quantity=10)
        self.store.add_product(new_product)
        self.assertIn(new_product, self.store.products)

    def test_add_existing_product(self):
        self.store.add_product(self.product1)  # Add the same product again
        self.assertEqual(len(self.store.products), 3)  # Should still be 3 products

    def test_remove_product(self):
        self.store.remove_product(self.product1)
        self.assertNotIn(self.product1, self.store.products)

    def test_remove_nonexistent_product(self):
        nonexistent_product = Product("Nonexistent Product", price=100, quantity=1)
        self.store.remove_product(nonexistent_product)  # Should not raise an error

    def test_get_total_quantity(self):
        total_quantity = self.store.get_total_quantity()
        self.assertEqual(total_quantity, 850)  # 100 + 500 + 250

    def test_display_products(self):
        # This is a side-effect test; we will just check if no exceptions are raised.
        try:
            self.store.display_products()
        except Exception as e:
            self.fail(f"display_products raised an exception: {e}")

    def test_order_valid(self):
        shopping_list = [(self.product1, 1), (self.product2, 2)]
        total_price = self.store.order(shopping_list)
        self.assertEqual(total_price, 1950)  # 1450 + 2 * 250

    def test_order_invalid_product(self):
        invalid_product = Product("Invalid Product", price=100, quantity=10)
        shopping_list = [(invalid_product, 1)]
        with self.assertRaises(ValueError):
            self.store.order(shopping_list)

    def test_make_order(self):
        # This test will check if `make_order` doesn't raise an exception.
        try:
            self.store.make_order()  # This will require user input; consider mocking it for a real test.
        except Exception as e:
            self.fail(f"make_order raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
