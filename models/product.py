class Product:
    def __init__(self, name: str, price: str, discount: str):
        self.name = name
        self.price = price
        self.discount = discount

    def __str__(self):
        return (f""
                f"{self.name}\n"
                f"Price: {self.price}\n"
                f"Discount: {self.discount}\n")