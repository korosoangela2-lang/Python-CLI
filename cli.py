import argparse
import importlib
import re

# Optional Rich support
try:
    rich_console = importlib.import_module("rich.console")
    rich_table = importlib.import_module("rich.table")
    Console = rich_console.Console
    Table = rich_table.Table
except ModuleNotFoundError:
    class Table:
        def __init__(self, title=""):
            self.title = title
            self.columns = []
            self.rows = []

        def add_column(self, name):
            self.columns.append(str(name))

        def add_row(self, *values):
            self.rows.append([str(v) for v in values])

        def __str__(self):
            if not self.columns:
                return self.title

            widths = [
                max(len(self.columns[i]), *(len(r[i]) for r in self.rows))
                for i in range(len(self.columns))
            ]

            header = " | ".join(
                self.columns[i].ljust(widths[i]) for i in range(len(self.columns))
            )
            separator = "-+-".join("-" * w for w in widths)

            rows = "\n".join(
                " | ".join(r[i].ljust(widths[i]) for i in range(len(self.columns)))
                for r in self.rows
            )

            return f"{self.title}\n{header}\n{separator}\n{rows}"

    class Console:
        def print(self, *objects, **kwargs):
            text = " ".join(str(o) for o in objects)
            text = re.sub(r"\[(?:/)?(?:green|red)\]", "", text)
            print(text)

console = Console()

from services import (
    add_user,
    get_users,
    add_budget,
    add_expense,
    pay_expense,
    search_budgets,
    budget_summary,
)


def list_users():
    """List all users in a formatted table."""
    users = get_users()
    table = Table(title="Users")
    table.add_column("Name")

    for u in users:
        table.add_row(u["name"])

    console.print(table)


def run_cli():
    parser = argparse.ArgumentParser(description="BudgetTrack CLI")
    subparsers = parser.add_subparsers(dest="command")

    # ---------------- USERS ----------------
    user_parser = subparsers.add_parser("add-user", help="Create a new user")
    user_parser.add_argument("--name", required=True)

    subparsers.add_parser("list-users", help="List all users")

    # ---------------- BUDGETS ----------------
    budget_parser = subparsers.add_parser("add-budget", help="Create a budget")
    budget_parser.add_argument("--user", required=True)
    budget_parser.add_argument("--title", required=True)

    search_parser = subparsers.add_parser("search-budgets", help="Search budgets by user")
    search_parser.add_argument("--user", required=True)

    summary_parser = subparsers.add_parser("budget-summary", help="Show budget summary")
    summary_parser.add_argument("--budget", required=True)

    # ---------------- EXPENSES ----------------
    expense_parser = subparsers.add_parser("add-expense", help="Add expense to budget")
    expense_parser.add_argument("--budget", required=True)
    expense_parser.add_argument("--title", required=True)
    expense_parser.add_argument("--amount", required=True, type=float)

    pay_parser = subparsers.add_parser("pay-expense", help="Mark expense as paid")
    pay_parser.add_argument("--budget", required=True)
    pay_parser.add_argument("--title", required=True)

    args = parser.parse_args()

    # ---------------- COMMAND HANDLERS ----------------

    if args.command == "add-user":
        add_user(args.name)
        console.print("[green]User Added[/green]")

    elif args.command == "list-users":
        list_users()


    elif args.command == "add-budget":
        add_budget(args.user, args.title)
        console.print("[green]Budget Added[/green]")

    elif args.command == "add-expense":
        add_expense(args.budget, args.title, args.amount)
        console.print("[green]Expense Added[/green]")

    elif args.command == "pay-expense":
        pay_expense(args.budget, args.title)
        console.print("[green]Expense Paid[/green]")

    elif args.command == "search-budgets":
        budgets = search_budgets(args.user)

        table = Table(title="Budgets")
        table.add_column("Title")
        table.add_column("Expenses")

        for b in budgets:
            table.add_row(b["title"], str(len(b.get("expenses", []))))

        console.print(table)

    elif args.command == "budget-summary":
        summary = budget_summary(args.budget)

        if summary:
            console.print(f"Budget: {summary['budget']}")
            console.print(f"Total: {summary['total']}")
            console.print(f"Paid: {summary['paid']}")
            console.print(f"Remaining: {summary['remaining']}")
        else:
            console.print("[red]Budget not found[/red]")

    else:
        parser.print_help()