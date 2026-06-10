#!/usr/bin/env python3

from cli import run_cli
from services import (
    add_user,
    get_users,
    add_budget,
    add_expense,
    pay_expense,
    search_budgets,
    budget_summary,
    add_project,
    add_task,
    complete_task,
    search_projects,
    project_summary,
)

__all__ = [
    "run_cli",
    "add_user",
    "get_users",
    "add_budget",
    "add_expense",
    "pay_expense",
    "search_budgets",
    "budget_summary",
    "add_project",
    "add_task",
    "complete_task",
    "search_projects",
    "project_summary",
]

if __name__ == "__main__":
    run_cli()
