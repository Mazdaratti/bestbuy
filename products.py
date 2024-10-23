from promotions import Promotion


class Product:
    """
    Represents a product in a store.

    Attributes:
        _name (str): The name of the product.
        _price (float): The price of the product.
        _quantity (int): The available quantity of the product.
        _active (bool): Indicates whether the product is active.
    """

    def __init__(self, name, price, quantity):
        """
        Initializes a new Product instance.

        Args:
            name (str): The name of the product.
            price (float): The price of the product. Must be a positive number.
            quantity (int): The initial quantity of the product. Must be a positive number.

        Raises:
            ValueError: If the name is empty, or if price or quantity are not positive numbers.
        """
        if not name:
            raise ValueError("Product name can not be empty.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price should be a positive number.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity should be a positive number.")
        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._promotion = None

    def __hash__(self):
        """
        Return the hash value of the product.

        The hash value is computed based on the product name, allowing
        Product instances to be used in hash-based collections like sets
        and dictionaries.

        Returns:
            int: The hash value of the product name.
        """
        return hash(self._name)

    def __eq__(self, other):
        """
        Compare two Product instances for equality based on name and price.

        Args:
            other (Product): The other Product instance to compare with.

        Returns:
            bool: True if the name and price are equal, False otherwise.
        """
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def __lt__(self, product):
        """Implements lower than comparison of product based on their prices"""
        return self._price < product.price

    def __gt__(self, product):
        """Implements greater than comparison of product based on their prices"""
        return self._price > product.price

    def __str__(self):
        """
        Displays the product details.

        Returns:
            str: The product details
        """
        if self.active:
            promotion_info = f"Promotion: {self.promotion.name}" if self.promotion else "Promotion: None"
            return f"Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}, {promotion_info}"
        return f"{self.name} is out of stock."

    @property
    def name(self):
        """gets the product name"""
        return self._name

    @property
    def price(self):
        """gets the product price"""
        return self._price

    @property
    def quantity(self):
        """
        Returns the current quantity of the product.

        Returns:
            int: The available quantity.
        """
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity):
        """
        Sets the quantity of the product and updates its active status.

        Args:
            new_quantity (int): The new quantity of the product. Must be a positive number.

        Raises:
            ValueError: If the quantity is not a positive integer.
        """
        if not isinstance(new_quantity, int) or new_quantity < 0:
            raise ValueError('Quantity should be a whole positive number.')
        self._quantity = new_quantity
        if self.quantity == 0:
            self.active = False

    @property
    def active(self):
        """
        Checks if the product is active.

        Returns:
            bool: True if the product is active, False otherwise.
        """
        return self._active

    @active.setter
    def active(self, value):
        """
        Sets the product's active state.

        Args:
            value (bool): True to activate the product, False to deactivate it.
        """
        if not isinstance(value, bool):
            raise ValueError("Active must be a boolean value.")
        self._active = value

    @property
    def promotion(self):
        """Gets the current promotion for the product."""
        return self._promotion

    @promotion.setter
    def promotion(self, promotion):
        """Sets the current promotion for the product."""
        if promotion and not isinstance(promotion, Promotion):
            raise ValueError("Promotion must be an instance of the Promotion class.")
        self._promotion = promotion

    def buy(self, quantity):
        """
        Attempts to buy the specified quantity of the product.

        Args:
            quantity (int): The number of items to purchase. Must be a positive number.

        Returns:
            float: The total cost of the purchase, rounded to two decimal places.

        Raises:
            ValueError: If the quantity to buy is not a positive integer or
            is greater than the available stock or if the product is inactive.
        """
        if not self.active:
            raise ValueError("Product Inactive")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a number greater than zero.")
        if self.quantity < quantity:
            raise ValueError(f"Quantity requested for {self.name} is larger than what exists.")

        # Update the quantity
        self.quantity = self.quantity - quantity

        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)

        return self._price * quantity


class NonStockedProduct(Product):
    """
    Represents a product that does not have stock, such as digital products.

    Non-stocked products always have a quantity of zero, and this quantity cannot
    be modified. For example, a software license might be considered non-stocked.

    Attributes:
        _name (str): The name of the product.
        _price (float): The price of the product.
        _quantity (int): Always set to 0 (non-stocked).
    """

    def __init__(self, name, price):
        """
        Initializes a NonStockedProduct with the given name and price.
        The quantity is set to 0 and cannot be changed.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
        """
        super().__init__(name, price, quantity=0)

    def __str__(self):
        """
        Displays the product details, indicating that the quantity is unlimited.

        Returns:
            str: The product details in the format "Name, Price: X, Quantity: Unlimited".
        """
        promotion_info = f"Promotion: {self.promotion.name}" if self.promotion else "Promotion: None"
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited, {promotion_info}"

    @property
    def quantity(self):
        """
        Overrides the quantity property to always return 0 for non-stocked products.

        Returns:
            int: Always returns 0.
        """
        return 0

    @quantity.setter
    def quantity(self, new_quantity):
        """
        Overrides the quantity setter to prevent changes to the quantity.
        Raises a ValueError if an attempt is made to modify the quantity.

        Raises:
            ValueError: Always raises an error since quantity cannot be modified.
        """
        raise ValueError("Cannot set quantity for a non-stocked product.")

    def buy(self, quantity):
        """
        Simulates purchasing a non-stocked product. The quantity requested does not
        affect the product's stock.

        Args:
            quantity (int): The number of items to purchase. Must be a positive integer.

        Returns:
            float: The total cost of the purchase.

        Raises:
            ValueError: If the quantity to buy is not a positive integer.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a number greater than zero.")

        # Calculate and return the total cost
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self._price * quantity


class LimitedProduct(Product):
    """
    Represents a product that has a maximum quantity limit per order.

    This class can be used for products like services (e.g., shipping fees) that
    can only be purchased a limited number of times per order.

    Attributes:
        _name (str): The name of the product.
        _price (float): The price of the product.
        _quantity (int): The available quantity of the product.
        _maximum (int): The maximum quantity that can be purchased in a single order.
    """

    def __init__(self, name, price, quantity, maximum):
        """
        Initializes a LimitedProduct with the given name, price, quantity, and maximum limit.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            quantity (int): The available quantity of the product.
            maximum (int): The maximum quantity allowed per order.
        """
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def __str__(self):
        """
        Displays the product details, including the maximum limit per order.

        Returns:
            str: The product details in the format "Name, Price: X,
                 Quantity: Limited to Y per order".
        """
        if self.active:
            promotion_info = f"Promotion: {self.promotion.name}" if self.promotion else "Promotion: None"
            return (f"{self.name}, Price: {self.price}, "
                    f"Quantity: Limited to {self.maximum} per order!, {promotion_info}")
        return f"{self.name} is out of stock."

    @property
    def maximum(self):
        """
        Returns the maximum quantity allowed per order for this product.

        Returns:
            int: The maximum quantity allowed per order.
        """
        return self._maximum

    def buy(self, quantity):
        """
        Attempts to buy the specified quantity of the product, enforcing the maximum limit.

        Args:
            quantity (int): The number of items to purchase. Must be a positive integer.

        Returns:
            float: The total cost of the purchase.

        Raises:
            ValueError: If the quantity to buy is greater than the allowed maximum,
                        if it exceeds the available stock, or if the product is inactive.
        """
        if not self.active:
            raise ValueError("Product Inactive")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a number greater than zero.")
        if quantity > self.maximum:
            raise ValueError(f"Only {self.maximum} is allowed from [{self.name}]!")
        if self.quantity < quantity:
            raise ValueError(f"Quantity requested for {self.name} is larger than what exists.")

        # Update the quantity
        self.quantity = self.quantity - quantity

        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)

        return self._price * quantity
