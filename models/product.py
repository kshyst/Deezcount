class Product:
    def __init__(self, name: str, price: str, discount: str):
        self.name = name
        self.price = price
        self.discount = discount

    def __str__(self):
        return (f""
                f"{self.name}\n"
                f"قیمت پایه : {self.price}\n"
                f"میزان تخفیف: {self.discount}\n"
                f"قیمت نهایی: {int(self.price) - int(self.discount)}\n"
                f"---------------------\n"
                )