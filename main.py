import sys
import products
import store


def exit_command(not_used):
    """
    Exits the program by printing a farewell message and terminating the process.
    """
    print("Thank you for visiting Best Buy! We hope to see you again soon."
          " Goodbye!")
    sys.exit(0)


def list_products(best_buy):
    products_list = [product.show() for product in best_buy.get_all_products()]
    print("-" * 6)
    for index, description in enumerate(products_list, start=1):
        print(f"{index}. {description}")
    print("-" * 6)


def show_total_amount(best_buy):
    print(f"Total of {best_buy.get_total_quantity()} items in store")


def make_order(best_buy):
    order_cart = {}
    order_items = []
    list_products(best_buy)
    print("When you want to finish the order, enter an empty text.")

    while True:
        active_products = best_buy.get_all_products()
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
            if not (1 <= product_index <= len(active_products)):
                raise ValueError("Invalid product index.")
            product = active_products[product_index - 1]
            if quantity < 1:
                raise ValueError("Invalid quantity.")
        except (ValueError, TypeError):
            print(f"Error adding product!")
            continue

        if product in order_cart:
            order_cart[product] += quantity
        else:
            order_cart[product] = quantity
        print("Product added to list!")

    order_items = [(product, amount) for product, amount in order_cart.items()]

    # Process the order
    if not order_items:
        print("No products to order!")
        return

    try:
        total_price = best_buy.order(order_items)
        if total_price:
            print("*" * 8)
            print(f"Order made! Total payment: ${total_price}.")
    except ValueError as e:
        print(f"Error while making order! {e}")


def display_menu(menu_entries):
    """
    Displays the menu to the user.
    Args:
        menu_entries (list): A list of tuples where each tuple contains a menu option description
                             and the corresponding function to call.
    """
    print("\n\tStore Menu")
    print("\t----------")
    for index, (description, _) in enumerate(menu_entries, start=1):
        print(f"{index}. {description}")


def get_user_choice(prompt, valid_range=None):
    """
    Prompts the user to make a choice and ensures the input is valid.

    Args:
        prompt (str): A prompt message to be displayed to the user.
        valid_range (range, list, or None): A range, list, or set of valid choices.
                                            If None, any input is accepted.

    Returns:
        int or None: The user's choice if valid, or None if the input is invalid.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            choice = int(user_input)
            if valid_range is None or choice in valid_range:
                return choice
            return None
        except ValueError:
            return None


def start(best_buy):
    menu_entries = [
        ("List all products in store", list_products),
        ("Show total amount in store", show_total_amount),
        ("Make an order", make_order),
        ("Quit", exit_command)
    ]
    while True:
        display_menu(menu_entries)
        choice = get_user_choice("Please choose a number: ", range(1, len(menu_entries) + 1))
        if not choice:
            print(f"Error with your choice! Try again.")
            continue
        menu_entries[choice - 1][1](best_buy)


def main():
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250)
                    ]

    best_buy = store.Store(product_list)

    start(best_buy)


if __name__ == "__main__":
    main()