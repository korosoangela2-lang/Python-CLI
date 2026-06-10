import storage

from services import (
    add_user,
    add_project,
    add_task,
    complete_task,
    search_projects,
    project_summary,
)


def setup_storage(tmp_path):
    storage.DATA_FILE = str(tmp_path / "data.json")
    storage.save_data([])


def test_project_workflow(tmp_path):
    setup_storage(tmp_path)

    add_user("Angela")
    add_project("Angela", "Launch Plan", "Project kickoff")
    add_task("Launch Plan", "Write docs", "Draft README", "2026-12-31")
    add_task("Launch Plan", "Deploy app", "Push to production", "2027-01-15")

    projects = search_projects("Angela")

    assert len(projects) == 1
    assert projects[0]["title"] == "Launch Plan"
    assert projects[0]["description"] == "Project kickoff"
    assert len(projects[0]["tasks"]) == 2


def test_complete_task_and_summary(tmp_path):
    setup_storage(tmp_path)

    add_user("Angela")
    add_project("Angela", "Launch Plan", "Project kickoff")
    add_task("Launch Plan", "Write docs", "Draft README")
    add_task("Launch Plan", "Deploy app", "Push to production")
    complete_task("Launch Plan", "Write docs")

    summary = project_summary("Launch Plan")

    assert summary == {
        "project": "Launch Plan",
        "total_tasks": 2,
        "completed_tasks": 1,
        "pending_tasks": 1,
        "completion_rate": 50.0,
    }


def test_complete_task_idempotent(tmp_path):
    setup_storage(tmp_path)

    add_user("Angela")
    add_project("Angela", "Launch Plan")
    add_task("Launch Plan", "Write docs", "Draft README")
    complete_task("Launch Plan", "Write docs")
    complete_task("Launch Plan", "Write docs")

    summary = project_summary("Launch Plan")

    assert summary["completed_tasks"] == 1
    assert summary["pending_tasks"] == 0
