class Expense:
    def __init__(self, title, amount, paid=False):
        self.title = title
        self.amount = float(amount)
        self.paid = paid

    def to_dict(self):
        return {
            "title": self.title,
            "amount": self.amount,
            "paid": self.paid
        }


class Budget:
    def __init__(self, title):
        self.title = title
        self.expenses = []

    def to_dict(self):
        return {
            "title": self.title,
            "expenses": self.expenses
        }


class User:
    def __init__(self, name):
        self.name = name
        self.budgets = []

    def to_dict(self):
        return {
            "name": self.name,
            "budgets": self.budgets
        }
