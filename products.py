class Product:
    def __init__(self, name, price, quantity):
        if not name:
            raise ValueError("Name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity += quantity
        if self.quantity <= 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self):
        if self.is_active():
            return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        return f"{self.name} is out of stock."

    def buy(self, quantity):
        if self.quantity >= quantity:
            self.set_quantity(- quantity)
            return self.price * quantity
        raise Exception("Quantity requested is larger than the available stock.")
