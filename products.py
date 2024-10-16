class Product:
    """
    Represents a product in a store.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The available quantity of the product.
        active (bool): Indicates whether the product is active.
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
            raise ValueError("Name cannot be empty.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price should be a positive number.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity should be a positive number.")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        """
        Returns the current quantity of the product.

        Returns:
            int: The available quantity.
        """
        return self.quantity

    def set_quantity(self, quantity):
        """
        Sets the quantity of the product and updates its active status.

        Args:
            quantity (int): The new quantity of the product. Must be a positive number.

        Raises:
            ValueError: If the quantity is not a positive integer.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Quantity should be a whole positive number.')
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self):
        """
        Checks if the product is active.

        Returns:
            bool: True if the product is active, False otherwise.
        """
        return self.active

    def activate(self):
        """
        Activates the product.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivates the product.
        """
        self.active = False

    def show(self):
        """
        Displays the product details.

        Returns:
            str: The product details if the product is active, otherwise indicates it's out of stock.
        """
        if self.is_active():
            return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        return f"{self.name} is out of stock."

    def buy(self, quantity):
        """
        Attempts to buy the specified quantity of the product.

        Args:
            quantity (int): The number of items to purchase. Must be a positive number.

        Returns:
            float: The total cost of the purchase, rounded to two decimal places.

        Raises:
            ValueError: If the quantity to buy is not a positive integer or is greater than the available stock or
                        if the product is inactive.
        """
        if not self.active:
            raise ValueError("Product Inactive")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a number greater than zero.")
        if self.quantity < quantity:
            raise ValueError(f"Quantity requested for {self.name} is larger than what exists.")

        # Update the quantity
        self.quantity -= quantity
        if self.quantity == 0:
            self.deactivate()
        # Calculate and return the total cost
        return round(self.price * quantity, 2)

