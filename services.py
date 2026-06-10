from storage import load_data, save_data


# =========================
# USER FUNCTIONS
# =========================

def add_user(name):
    users = load_data()

    users.append({
        "name": name,
        "budgets": [],
        "projects": []
    })

    save_data(users)


def get_users():
    return load_data()


# =========================
# BUDGET FUNCTIONS
# =========================

def add_budget(user_name, title):
    users = load_data()

    for user in users:
        if user["name"].lower() == user_name.lower():
            user.setdefault("budgets", [])

            # prevent duplicates
            if any(b["title"].lower() == title.lower() for b in user["budgets"]):
                return False

            user["budgets"].append({
                "title": title,
                "expenses": []
            })

            save_data(users)
            return True

    return False


def add_expense(budget_title, title, amount):
    users = load_data()

    for user in users:
        for budget in user.get("budgets", []):
            if budget["title"].lower() == budget_title.lower():

                budget.setdefault("expenses", []).append({
                    "title": title,
                    "amount": float(amount),
                    "paid": False
                })

                save_data(users)
                return True

    return False


def pay_expense(budget_title, expense_title):
    users = load_data()

    for user in users:
        for budget in user.get("budgets", []):
            if budget["title"].lower() == budget_title.lower():

                for expense in budget.get("expenses", []):
                    if expense["title"].lower() == expense_title.lower():
                        expense["paid"] = True
                        save_data(users)
                        return True

    return False


def search_budgets(user_name):
    users = load_data()

    for user in users:
        if user["name"].lower() == user_name.lower():
            return user.get("budgets", [])

    return []


def budget_summary(budget_title):
    users = load_data()

    for user in users:
        for budget in user.get("budgets", []):
            if budget["title"].lower() == budget_title.lower():

                expenses = budget.get("expenses", [])

                total = sum(e["amount"] for e in expenses)
                paid = sum(e["amount"] for e in expenses if e.get("paid"))
                remaining = total - paid

                return {
                    "budget": budget["title"],
                    "total": total,
                    "paid": paid,
                    "remaining": remaining
                }

    return None


# =========================
# PROJECT FUNCTIONS
# =========================

def _find_user(users, name):
    return next(
        (u for u in users if u.get("name", "").lower() == name.lower()),
        None
    )


def _find_project(users, project_title):
    for user in users:
        for project in user.get("projects", []):
            if project.get("title", "").lower() == project_title.lower():
                return project
    return None


def add_project(user_name, title, description=""):
    users = load_data()
    user = _find_user(users, user_name)

    if not user:
        return False

    user.setdefault("projects", [])

    if any(p["title"].lower() == title.lower() for p in user["projects"]):
        return False

    user["projects"].append({
        "title": title,
        "description": description,
        "tasks": []
    })

    save_data(users)
    return True


def add_task(project_title, title, description="", due_date=None):
    users = load_data()
    project = _find_project(users, project_title)

    if not project:
        return False

    project.setdefault("tasks", []).append({
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    })

    save_data(users)
    return True


def complete_task(project_title, task_title):
    users = load_data()
    project = _find_project(users, project_title)

    if not project:
        return False

    for task in project.get("tasks", []):
        if task["title"].lower() == task_title.lower():
            if not task.get("completed"):
                task["completed"] = True
                save_data(users)
                return True

    return False


def search_projects(user_name):
    users = load_data()
    user = _find_user(users, user_name)

    return user.get("projects", []) if user else []


def project_summary(project_title):
    users = load_data()
    project = _find_project(users, project_title)

    if not project:
        return None

    tasks = project.get("tasks", [])

    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed"))
    pending = total - completed
    rate = round((completed / total) * 100, 1) if total else 0.0

    return {
        "project": project["title"],
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_rate": rate
    }