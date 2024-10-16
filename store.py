class Store:
    """
        A class to represent a store that manages a collection of products.

        The Store class allows adding, removing, and querying products.
        It also facilitates processing orders for multiple products, calculating the total cost,
        and managing inventory quantities.

        Attributes:
            products (list): A list of Product instances available in the store.
        """

    def __init__(self, products=None):
        """
        Initializes the store with a list of products.

        Args:
            products (list, optional): A list of Product instances to add to the store.
                                       Defaults to an empty list if not provided.
        """
        self.products = products if products else []

    def add_product(self, product):
        """
        Adds a product to the store.

        Args:
            product (Product): The product instance to be added.

        Raises:
            ValueError: If the product is already in the store.
        """

        if product.name not in [item.name for item in self.products]:
            self.products.append(product)
            print(f"{product.name} is successfully added to the store.")
        else:
            print(f"{product.name} is already in store.")

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

    def display_products(self):
        """
        Lists all the products available in the store.
        """
        products_list = [product.show() for product in self.get_all_products()]
        print("-" * 6)
        for index, description in enumerate(products_list, start=1):
            print(f"{index}. {description}")
        print("-" * 6)

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
            else:
                total_price += product.buy(quantity)
        return total_price

    def make_order(self):
        """
        Handles the process of making an order by prompting the user for product and quantity.
        Validates inputs and updates the store accordingly.
        """
        order_items = []
        self.display_products()  # List products available in the store.
        print("When you want to finish the order, enter an empty text.")

        while True:
            active_products = self.get_all_products()
            if not active_products:
                print("No products available for ordering.")
                break

            product, quantity = self.get_order_input(active_products)

            if product is None and quantity is None:  # User wants to finish ordering
                break

            if product and quantity:  # Valid product and quantity
                order_items.append((product, quantity))  # Add to order
                print("Product added to list!")

        self.process_order(order_items)

    def get_order_input(self, active_products):
        """
        Prompts the user for product and quantity input, validates them, and returns the values.

        Args:
            active_products (list): The list of available products.

        Returns:
            tuple: (Product, quantity) if valid, (None, None) if the user wants to finish.
        """
        product_input = input("Which product # do you want? ").strip()
        quantity_input = input("What amount do you want? ").strip()

        if not product_input or not quantity_input:
            return None, None  # User wants to finish ordering

        try:
            product, quantity = self.validate_order_input(product_input, quantity_input, active_products)
            return product, quantity
        except ValueError as e:
            print(f"Error adding product: {e}")
            return None, None  # Return None to indicate invalid input

    def validate_order_input(self, product_input, quantity_input, active_products):
        """
        Validates the product and quantity inputs provided by the user.

        Args:
            product_input (str): The product index input from the user.
            quantity_input (str): The quantity input from the user.
            active_products (list): The list of available products.

        Returns:
            tuple: (product, quantity) if valid, raises a ValueError otherwise.
        """
        try:
            product_index = int(product_input)
            quantity = int(quantity_input)

            if not (1 <= product_index <= len(active_products)):
                raise ValueError("Invalid product index.")
            product = active_products[product_index - 1]

            if quantity < 1:
                raise ValueError("Invalid quantity.")
            return product, quantity
        except (ValueError, TypeError):
            raise ValueError("Error adding product! Please enter a valid product number and quantity.")

    def process_order(self, order_items):
        """
        Processes the final order and displays the total cost.

        Args:
            order_items (list): A list of tuples containing product and quantity.
        """
        if not order_items:
            print("No products to order!")
            return

        try:
            total_price = self.order(order_items)
            if total_price:
                print("*" * 8)
                print(f"Order made! Total payment: ${total_price:.2f}.")
        except ValueError as e:
            print(f"Error while making order: {e}")

