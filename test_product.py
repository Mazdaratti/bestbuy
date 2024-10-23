import pytest
from products import Product


def test_product_initialization():
    """
    Test the initialization of the Product class.

    Ensure the product instance is created successfully.
    """
    assert isinstance(Product("MacBook Air M2", price=1200, quantity=12), Product), (
        "Valid Product isn't created"
    )


def test_empty_name():
    """
    Test that Product creation with an empty name raises a ValueError.
    """
    with pytest.raises(ValueError, match='Product name can not be empty.'):
        Product("", price=1450, quantity=100)


def test_negative_price():
    """
    Test that Product creation with a negative price raises a ValueError.
    """
    with pytest.raises(ValueError, match='Price should be a positive number.'):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_negative_quantity():
    """
    Test that Product creation with a negative quantity raises a ValueError.
    """
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("MacBook Air M2", price=144, quantity=-12.3)


def test_float_quantity():
    """
    Test that Product creation with a float quantity raises a ValueError.
    """
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("Macbook Air M2", price=144, quantity=20.4)


def test_product_hash():
    """
    Test that the hash of the product is based on the name.

    Products with the same name should have the same hash.
    """
    product1 = Product("Apple", 1.5, 10)
    product2 = Product("Apple", 1.5, 5)

    assert hash(product1) == hash(product2)

    # Test different names result in different hashes
    product3 = Product("Orange", 1.2, 5)
    assert hash(product1) != hash(product3)


def test_product_str():
    """
    Test the __str__ method for displaying the product details.
    """
    product = Product("Apple", 1.5, 10)
    assert str(product) == "Apple, Price: 1.5, Quantity: 10"


def test_product_becomes_inactive():
    """
    Test that when a product reaches 0 quantity, it becomes inactive.
    """
    mac = Product("Macbook Air M2", price=1212, quantity=2)
    mac.quantity = 0
    assert not mac.active, "Product didn't become inactive when it reached 0 quantity"


def test_product_name_getter():
    """
    Test that the product name is returned correctly via the property.
    """
    product = Product("Banana", 0.5, 20)
    assert product.name == "Banana"


def test_product_price_getter():
    """
    Test that the product price is returned correctly via the property.
    """
    product = Product("Banana", 0.5, 20)
    assert product.price == 0.5


def test_product_quantity_getter():
    """
    Test that the quantity getter returns the correct value.
    """
    product = Product("Banana", 0.5, 20)
    assert product.quantity == 20


def test_product_quantity_setter():
    """
    Test setting a new quantity for the product.

    Ensure that setting a valid quantity updates the product correctly.
    """
    product = Product("Banana", 0.5, 20)
    product.quantity = 15
    assert product.quantity == 15

    # Test setting the quantity to zero
    product.quantity = 0
    assert product.quantity == 0
    assert product.active is False

    # Test setting an invalid quantity
    with pytest.raises(ValueError):
        product.quantity = -5


def test_product_activation():
    """
    Test the activation and deactivation of a product.

    The product's active status should change when the active setter is used.
    """
    product = Product("Apple", 1.5, 10)
    product.active = False
    assert not product.active

    product.active = True
    assert product.active


def test_product_buy():
    """
    Test buying a specified quantity of the product.

    Ensure the product quantity updates correctly after purchase.
    """
    product = Product("Apple", 1.5, 10)
    total_cost = product.buy(2)
    assert total_cost == 3.0
    assert product.quantity == 8

    # Test buying more than available stock
    with pytest.raises(ValueError, match="Quantity requested for Apple is larger"):
        product.buy(15)

    # Test buying when the product is inactive
    product.active = False
    with pytest.raises(ValueError, match="Product Inactive"):
        product.buy(1)


def test_product_buy_invalid_quantity():
    """
    Test buying with invalid quantities.

    Buying with non-positive quantities should raise a ValueError.
    """
    product = Product("Apple", 1.5, 10)

    # Test buying with quantity <= 0
    with pytest.raises(ValueError, match="Quantity to buy must be a number greater than zero."):
        product.buy(0)

    with pytest.raises(ValueError, match="Quantity to buy must be a number greater than zero."):
        product.buy(-3)


def test_product_eq():
    """
    Test the equality comparison (__eq__) for two products.

    Products are considered equal if they have the same name and price.
    """
    product1 = Product("Apple", 1.5, 10)
    product2 = Product("Apple", 1.5, 5)
    product3 = Product("Orange", 1.2, 5)

    assert product1 == product2, "Products with the same name and price should be equal"
    assert product1 != product3, "Products with different names or prices should not be equal"


def test_product_lt_gt():
    """
    Test the less-than and greater-than comparison for products.

    Products are compared based on their prices.
    """
    product1 = Product("Apple", 1.5, 10)
    product2 = Product("Orange", 1.2, 5)

    assert product2 < product1, "Product with lower price should be less than product with higher price"
    assert product1 > product2, "Product with higher price should be greater than product with lower price"

