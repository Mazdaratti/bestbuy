import pytest
from products import Product, NonStockedProduct, LimitedProduct
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store


@pytest.fixture
def setup_products():
    """Fixture to set up sample products for testing."""
    product1 = Product("MacBook Air M2", price=1450, quantity=100)
    product2 = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    product3 = NonStockedProduct("Windows License", price=125)
    product4 = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    # Assign promotions
    promo_half_price = SecondHalfPrice("Second Half price!")
    promo_third_free = ThirdOneFree("Third One Free!")
    promo_30_percent = PercentDiscount("30% off!", percent=30)

    product1.promotion = promo_half_price
    product2.promotion = promo_third_free
    product3.promotion = promo_30_percent

    return product1, product2, product3, product4


@pytest.fixture
def setup_store(setup_products):
    """Fixture to set up a store with products for testing."""
    return Store(list(setup_products))


def test_product_initialization():
    """Test the initialization of the Product class."""
    product = Product("MacBook Air M2", price=1200, quantity=12)
    assert isinstance(product, Product), "Valid Product isn't created"


def test_empty_name():
    """Test that Product creation with an empty name raises a ValueError."""
    with pytest.raises(ValueError, match='Product name can not be empty.'):
        Product("", price=1450, quantity=100)


def test_negative_price():
    """Test that Product creation with a negative price raises a ValueError."""
    with pytest.raises(ValueError, match='Price should be a positive number.'):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_negative_quantity():
    """Test that Product creation with a negative quantity raises a ValueError."""
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("MacBook Air M2", price=144, quantity=-12.3)


def test_float_quantity():
    """Test that Product creation with a float quantity raises a ValueError."""
    with pytest.raises(ValueError, match='Quantity should be a positive number.'):
        Product("Macbook Air M2", price=144, quantity=20.4)


def test_product_hash():
    """Test that the hash of the product is based on the name."""
    product1 = Product("Apple", 1.5, 10)
    product2 = Product("Apple", 1.5, 5)

    assert hash(product1) == hash(product2)

    # Test different names result in different hashes
    product3 = Product("Orange", 1.2, 5)
    assert hash(product1) != hash(product3)


def test_product_str():
    """Test the __str__ method for displaying the product details."""
    product = Product("Apple", 1.5, 10)
    assert str(product) == "Name: Apple, Price: 1.5, Quantity: 10, Promotion: None"

    # Test with an active product with a promotion
    mock_promotion = PercentDiscount(name="10% Off", percent=10)
    product.promotion = mock_promotion
    assert str(product) == "Name: Apple, Price: 1.5, Quantity: 10, Promotion: 10% Off"

    # Test with an inactive product
    product.active = False
    assert str(product) == "Apple is out of stock."


def test_product_becomes_inactive():
    """Test that when a product reaches 0 quantity, it becomes inactive."""
    mac = Product("Macbook Air M2", price=1212, quantity=2)
    mac.quantity = 0
    assert not mac.active, "Product didn't become inactive when it reached 0 quantity"


def test_product_name_getter():
    """Test that the product name is returned correctly via the property."""
    product = Product("Banana", 0.5, 20)
    assert product.name == "Banana"


def test_product_price_getter():
    """Test that the product price is returned correctly via the property."""
    product = Product("Banana", 0.5, 20)
    assert product.price == 0.5


def test_product_quantity_getter():
    """Test that the quantity getter returns the correct value."""
    product = Product("Banana", 0.5, 20)
    assert product.quantity == 20


def test_product_quantity_setter():
    """Test setting a new quantity for the product."""
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
    """Test the activation and deactivation of a product."""
    product = Product("Apple", 1.5, 10)
    product.active = False
    assert not product.active

    product.active = True
    assert product.active


def test_product_buy():
    """Test buying a specified quantity of the product."""
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
    """Test buying with invalid quantities."""
    product = Product("Apple", 1.5, 10)

    # Test buying with quantity <= 0
    with pytest.raises(ValueError, match="Quantity to buy must be "
                                         "a number greater than zero."):
        product.buy(0)

    with pytest.raises(ValueError, match="Quantity to buy must be "
                                         "a number greater than zero."):
        product.buy(-3)


def test_product_eq():
    """Test the equality comparison (__eq__) for two products."""
    product1 = Product("Apple", 1.5, 10)
    product2 = Product("Apple", 1.5, 5)
    product3 = Product("Orange", 1.2, 5)

    assert product1 == product2, ("Products with the same name and price"
                                  " should be equal")
    assert product1 != product3, ("Products with different names or prices"
                                  " should not be equal")


def test_product_lt_gt():
    """Test the less-than and greater-than comparison for products."""
    product1 = Product("Apple", 1.5, 10)
    product2 = Product("Orange", 1.2, 5)

    assert product2 < product1, ("Product with lower price should be "
                                 "less than product with higher price")
    assert product1 > product2, ("Product with higher price should be "
                                 "greater than product with lower price")


# NonStockedProduct tests
def test_nonstocked_product_initialization():
    """Test the initialization of the NonStockedProduct class."""
    product = NonStockedProduct("E-Book", price=10)
    assert isinstance(product, NonStockedProduct)
    assert product.quantity == 0
    assert str(product) == ("E-Book, Price: 10, Quantity: Unlimited,"
                            " Promotion: None")


def test_nonstocked_product_quantity_setter():
    """
    Test that attempting to set the quantity of a NonStockedProduct
    raises a ValueError.
    """
    product = NonStockedProduct("E-Book", price=10)
    with pytest.raises(ValueError, match="Cannot set quantity for "
                                         "a non-stocked product."):
        product.quantity = 5


def test_nonstocked_product_buy():
    """Test the buy method for NonStockedProduct."""
    product = NonStockedProduct("E-Book", price=10)
    total_cost = product.buy(3)
    assert total_cost == 30

    with pytest.raises(ValueError, match="Quantity to buy must be a number "
                                         "greater than zero."):
        product.buy(-1)


# LimitedProduct tests
def test_limited_product_initialization():
    """Test the initialization of the LimitedProduct class."""
    product = LimitedProduct("Shipping Fee", price=5, quantity=10, maximum=2)
    assert isinstance(product, LimitedProduct)
    assert product.maximum == 2
    assert str(product) == ("Shipping Fee, Price: 5, "
                            "Quantity: Limited to 2 per order!, Promotion: None")


def test_limited_product_buy_within_limit():
    """Test the buy method of LimitedProduct when buying within the limit."""
    product = LimitedProduct("Shipping Fee", price=5, quantity=10, maximum=2)
    total_cost = product.buy(2)
    assert total_cost == 10
    assert product.quantity == 8


def test_limited_product_buy_exceeds_limit():
    """Test that attempting to buy more than the allowed maximum raises a ValueError."""
    product = LimitedProduct("Shipping Fee", price=5, quantity=10, maximum=2)
    with pytest.raises(ValueError, match="Only 2 is allowed from \\[Shipping Fee\\]!"):
        product.buy(3)


def test_limited_product_buy_exceeds_stock():
    """Test that attempting to buy more than available stock raises a ValueError."""
    product = LimitedProduct("Shipping Fee", price=5, quantity=1, maximum=2)
    with pytest.raises(ValueError, match="Quantity requested for Shipping Fee "
                                         "is larger than what exists"):
        product.buy(2)


# Promotions tests
def test_second_half_price_promotion(setup_products):
    """Test the second half-price promotion."""
    product1, _, _, _ = setup_products
    total_cost = product1.buy(2)  # Second one should be half price
    assert total_cost == 1450 * 1.5


def test_third_one_free_promotion(setup_products):
    """Test the third-one-free promotion."""
    _, product2, _, _ = setup_products
    total_cost = product2.buy(3)  # Should only pay for two
    assert total_cost == 250 * 2


def test_percent_discount_promotion(setup_products):
    """Test the percentage discount promotion."""
    _, _, product3, _ = setup_products
    total_cost = product3.buy(1)
    assert total_cost == 125 * 0.7  # 30% off


def test_limited_product(setup_products):
    """Test that a limited product cannot be purchased in excess
       of the maximum quantity."""
    _, _, _, product4 = setup_products
    with pytest.raises(ValueError):
        product4.buy(2)  # Should not allow more than 1
    total_cost = product4.buy(1)
    assert total_cost == 10


# Store tests
def test_add_product(setup_store):
    """Test that products can be added to the store."""
    store = setup_store
    new_product = Product("iPhone 14", price=999, quantity=200)
    store.add_product(new_product)
    assert new_product in store.all_products


def test_remove_product(setup_store):
    """Test that products can be removed from the store."""
    store = setup_store
    product_to_remove = store.all_products[1]  # Remove the second product
    store.remove_product(product_to_remove)
    assert product_to_remove not in store.all_products


def test_total_quantity(setup_store):
    """Test that total quantity is calculated correctly."""
    store = setup_store
    assert store.total_quantity == 100 + 500 + 250


def test_list_active_products(setup_store):
    """
    Test that the total quantity is equal to the sum of quantities
    of all active products.
    """
    store = setup_store
    # Calculate the total quantity of all stocked products
    total_quantity = sum(product.quantity for product in store.all_products
                         if product.quantity is not None)

    assert store.total_quantity == total_quantity


def test_order_with_valid_products(setup_store):
    """Test that an order with valid products processes correctly."""
    store = setup_store
    shopping_list = [(store.all_products[0], 2), (store.all_products[1], 3)]
    total_cost = store.order(shopping_list)
    assert total_cost == store.all_products[0].buy(2) + store.all_products[1].buy(3)


def test_order_with_invalid_product(setup_store):
    """Test that an order with a product not in the store raises an error."""
    store = setup_store
    invalid_product = Product("Invalid Product", price=100, quantity=10)
    with pytest.raises(ValueError):
        store.order([(invalid_product, 1)])


import pytest


# Assuming Store is imported or defined above this line
# from your_module import Store

@pytest.fixture
def stores():
    """Fixture to create example store instances."""
    store1 = Store([
        {"name": "Product A", "quantity": 10, "price": 5.0},
        {"name": "Product B", "quantity": 5, "price": 10.0}
    ])
    store2 = Store([
        {"name": "Product C", "quantity": 3, "price": 7.0},
        {"name": "Product D", "quantity": 2, "price": 15.0}
    ])
    empty_store = Store([])

    return store1, store2, empty_store


def test_add_stores(stores):
    """Test combining two stores into a new Store instance."""
    store1, store2, _ = stores
    combined_store = store1 + store2

    expected_products = [
        {"name": "Product A", "quantity": 10, "price": 5.0},
        {"name": "Product B", "quantity": 5, "price": 10.0},
        {"name": "Product C", "quantity": 3, "price": 7.0},
        {"name": "Product D", "quantity": 2, "price": 15.0}
    ]

    # Check that the combined store has the expected products
    assert combined_store._products == expected_products
    # Check the length of the combined products
    assert len(combined_store._products) == 4


def test_add_invalid_type(stores):
    """Test adding a non-Store instance raises ValueError."""
    store1, _, _ = stores
    with pytest.raises(ValueError, match="Can only combine with another Store instance."):
        result = store1 + "not_a_store"


def test_add_empty_store(stores):
    """Test combining a store with an empty store."""
    store1, _, empty_store = stores
    combined_store = store1 + empty_store

    # The result should be the same as store1
    assert combined_store._products == store1._products
