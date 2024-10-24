import sys
import products
import store
import promotions


def display_menu():
    """
    Displays the menu to the user.
    """
    print("\n\tStore Menu")
    print("\t----------")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit")


def start(best_buy):
    """
    Starts the interactive store program.

    Args:
        best_buy (Store): The store instance containing the products.
    """
    while True:
        display_menu()
        choice = input("Please choose a number: ").strip()
        if choice == '1':
            best_buy.display_products()
        elif choice == '2':
            print(f"Total of {best_buy.total_quantity} items in store")
        elif choice == '3':
            best_buy.make_order()
        elif choice == '4':
            print("Thanks for visiting Best Buy Shop! Bye!")
            sys.exit(0)
        else:
            print("Error with your choice! Try again.")


def main():
    """
    Main function to initialize the store and start the program.
    """
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[3].promotion = thirty_percent

    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
