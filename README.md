# BudgetTrack CLI

A simple Python command-line application for managing users, budgets, and expenses.

## Features

- Add users
- List users
- Create budgets for users
- Add expenses to budgets
- Mark expenses as paid
- Search budgets by user
- View a budget summary

## Setup

1. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main CLI application directly:

```bash
./budgettrack <command> [options]
```

If you prefer, you can also run the script directly:

```bash
./main.py <command> [options]
```

### Commands

- `add-user --name <name>`
- `list-users`
- `add-budget --user <name> --title <title>`
- `add-expense --budget <title> --title <title> --amount <amount>`
- `pay-expense --budget <title> --expense <title>`
- `search-budgets --user <name>`
- `budget-summary --budget <title>`

### Examples

Add a new user:

```bash
python main.py add-user --name Angela
```

Create a budget for a user:

```bash
python main.py add-budget --user Angela --title "Personal Budget"
```

Add expenses to the budget:

```bash
python main.py add-expense --budget "Personal Budget" --title "Rent" --amount 15000
python main.py add-expense --budget "Personal Budget" --title "Food" --amount 5000
```

Mark an expense as paid:

```bash
python main.py pay-expense --budget "Personal Budget" --expense "Rent"
```

Search budgets for a user:

```bash
python main.py search-budgets --user Angela
```

View a budget summary:

```bash
python main.py budget-summary --budget "Personal Budget"
```

## Data Persistence

Budget and expense entries are saved to `data.json` in the repository root.

## Testing

Run tests with:

```bash
pytest -q
```
