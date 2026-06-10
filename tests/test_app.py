from models import User, Budget, Expense


def test_user_creation():
    user = User("Angela")

    assert user.name == "Angela"


def test_budget_creation():
    budget = Budget("Personal Budget")

    assert budget.title == "Personal Budget"


def test_expense_creation():
    expense = Expense("Rent", 15000)

    assert expense.amount == 15000


def test_expense_paid():
    expense = Expense("Rent", 15000)

    expense.paid = True

    assert expense.paid is True
