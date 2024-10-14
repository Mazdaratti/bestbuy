class Store:
    def __init__(self, products=None):
        """
        Initializes the store with a list of products.

        Args:
            products (list, optional): A list of Product instances to add to the store.
                                       Defaults to an empty list if not provided.
        """
        self.products = products if products else []

    def remove_product(self, product):
        """
        Removes a product from the store.

        Args:
            product (Product): The product instance to be removed.

        Raises:
            ValueError: If the product is not found in the store.
        """
        if product in self.products:
            self.products.remove(product)
            print(f"{product.name} is successfully removed from the store.")
        else:
            print(f"No {product.name} in store.")

    def add_product(self, product):
        """
        Adds a product to the store.

        Args:
            product (Product): The product instance to be added.

        Raises:
            ValueError: If the product is already in the store.
        """
        if product not in self.products:
            self.products.append(product)
            print(f"{product.name} is successfully added to the store.")
        else:
            print(f"{product.name} is already in store.")

    def get_total_quantity(self) -> int:
        """
        Calculates the total quantity of all products in the store.

        Returns:
            int: The total quantity of products.
        """
        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> list:
        """
        Retrieves all active products in the store.

        Returns:
            list: A list of active Product instances.
        """
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list) -> float:
        """
        Processes an order for multiple products.

        Args:
            shopping_list (list): A list of tuples, where each tuple contains a
                                  Product instance and a quantity.

        Returns:
            float: The total cost of the order.

        Raises:
            ValueError: If the product is not in the store or the quantity is invalid.
        """
        total_price = 0
        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError(f'There is no {product.name} in the store.')
            try:
                total_price += product.buy(quantity)
            except ValueError as e:
                print(f"Invalid quantity for {product.name}: {e}")
        return total_price

