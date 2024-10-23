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
        self._products = products if products else []

    def __contains__(self, product):
        """
        Check if the given Product object matches this product.

        Args:
            product (Product): The Product object to check.

        Returns:
            bool: True if the Product name matches this product's name, False otherwise.
        """
        return product in self._products

    def add_product(self, product):
        """
        Adds a product to the store.

        Args:
            product (Product): The product instance to be added.

        Raises:
            ValueError: If the product is already in the store.
        """

        if product not in self._products:
            self._products.append(product)
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
        if product in self._products:
            self._products.remove(product)
            print(f"{product.name} is successfully removed from the store.")
        else:
            print(f"No {product.name} in store.")

    @property
    def total_quantity(self) -> int:
        """
        Calculates the total quantity of all products in the store.

        Returns:
            int: The total quantity of products.
        """
        return sum(product.quantity for product in self._products)

    @property
    def all_products(self) -> list:
        """
        Retrieves all active products in the store.

        Returns:
            list: A list of active Product instances.
        """
        return [product for product in self._products if product.active]

    def display_products(self):
        """
        Lists all the products available in the store.
        """
        print("-" * 6)
        for index, product in enumerate(self.all_products, start=1):
            print(f"{index}. {product}")
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
            ValueError: If the product is not in the store or
                        the quantity is invalid.
        """
        total_price = 0
        for product, quantity in shopping_list:
            if product not in self._products:
                raise ValueError(f'There is no {product.name} in the store.')
            total_price += product.buy(quantity)
        return total_price

    def make_order(self):
        """
        Handles the process of making an order by prompting
        the user for product and quantity.
        Validates inputs and updates the store accordingly.
        """
        order_cart = {}
        self.display_products()
        print("When you want to finish the order, enter an empty text.")

        while True:
            active_products = self.all_products
            if not active_products:
                print("No products available for ordering.")
                break

            product_input = input("Which product # do you want? ").strip()
            quantity_input = input("What amount do you want? ").strip()

            if not product_input or not quantity_input:
                break

            try:
                product_index = int(product_input)
                quantity = int(quantity_input)
                if not 1 <= product_index <= len(active_products):
                    raise ValueError("Invalid product index.")
                product = active_products[product_index - 1]
                if quantity < 1:
                    raise ValueError("Invalid quantity.")
            except (ValueError, TypeError):
                print("Error adding product!\n")
                continue

            # Update the quantity in the order cart
            if product in order_cart:
                order_cart[product] += quantity
            else:
                order_cart[product] = quantity

            print("Product added to list!\n")

        self.process_order(order_cart)

    def process_order(self, order_cart):
        """
        Processes the final order and displays the total cost.

        Args:
            order_cart (dict): A dictionary containing product and quantity.
        """
        order_items = list(order_cart.items())

        if not order_items:
            print("No products to order!")
            return

        try:
            total_price = self.order(order_items)
            if total_price:
                print("*" * 8)
                print(f"Order made! Total payment: ${total_price:.2f}.")
        except ValueError as amount_error:
            print(f"Error while making order! {amount_error}")