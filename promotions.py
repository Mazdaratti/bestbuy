from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Abstract base class for different promotion types.

    Attributes:
        _name (str): The name of the promotion.
    """

    def __init__(self, name):
        """
        Initializes the promotion with a given name.

        Args:
            name (str): The name of the promotion.
        """
        self._name = name

    def __str__(self):
        """
        Returns the string representation of the promotion (its name).

        Returns:
            str: The name of the promotion.
        """
        return self._name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """
        Abstract method to apply the promotion to a given product and quantity.

        Args:
            product (Product): The product to which the promotion applies.
            quantity (int): The quantity of the product being purchased.

        Returns:
            float: The discount coefficient to be applied to the price.
        """
        pass


class SecondHalfPrice(Promotion):
    """
    Promotion where the second item is half-price.

    This promotion applies if the quantity of products is 2 or more.
    """

    def apply_promotion(self, product, quantity):
        """
        Applies the second half-price promotion.

        If the quantity is 2 or more, it calculates the discount coefficient.
        The formula gives half price for every second item.

        Args:
            product (Product): The product to which the promotion applies.
            quantity (int): The quantity of the product being purchased.

        Returns:
            float: The discount coefficient to be applied to the price.
        """
        if quantity >= 2:
            return product.price * ((quantity // 2) * 1.5 + quantity % 2)
        return product.price * quantity


class ThirdOneFree(Promotion):
    """
    Promotion where every third item is free.

    This promotion applies if the quantity of products is 3 or more.
    """

    def apply_promotion(self, product, quantity):
        """
        Applies the 'third one free' promotion.

        If the quantity is 3 or more, it calculates the discount coefficient.
        For every three items, the third one is free.

        Args:
            product (Product): The product to which the promotion applies.
            quantity (int): The quantity of the product being purchased.

        Returns:
            float: The discount coefficient to be applied to the price.
        """
        if quantity >= 3:
            return product.price * (quantity - (quantity // 3))
        return product.price * quantity


class PercentDiscount(Promotion):
    """
    Promotion that applies a percentage discount to the product.

    This promotion reduces the price by a fixed percentage.
    """

    def __init__(self, name, percent):
        """
        Initializes the percentage discount promotion.

        Args:
            name (str): The name of the promotion.
            percent (float): The percentage discount to be applied.
        """
        super().__init__(name)
        self._percent = percent

    def apply_promotion(self, product, quantity):
        """
        Applies the percentage discount promotion.

        Reduces the product's price by the given percentage, regardless of quantity.

        Args:
            product (Product): The product to which the promotion applies.
            quantity (int): The quantity of the product being purchased.

        Returns:
            float: The discount coefficient to be applied to the price.
        """
        return product.price * (100 - self._percent) / 100
