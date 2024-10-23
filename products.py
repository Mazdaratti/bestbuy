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
        return f"{self.name}, Price: {self._price}, Quantity: {self._quantity}"

    @property
    def name(self):
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

        # Calculate and return the total cost
        return self._price * quantity