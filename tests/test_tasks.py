from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.models.task_model import Category, Priority, RecurrenceType, Tag


def test_create_task(client: TestClient):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "priority": "high",
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] == task_data["completed"]
    assert "id" in data
    assert "created_at" in data


def test_read_tasks(client: TestClient):
    # Create test tasks
    task_data = [
        {"title": "Task 1", "description": "Description 1"},
        {"title": "Task 2", "description": "Description 2"},
    ]

    for task in task_data:
        client.post("/api/v1/tasks/", json=task)

    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_read_task(client: TestClient):
    # Create a test task
    task_data = {"title": "Single Task", "description": "Test Description"}
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]


def test_read_nonexistent_task(client: TestClient):
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client: TestClient):
    # Create a test task
    task_data = {"title": "Original Title", "description": "Original Description"}
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True,
    }
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["completed"] == update_data["completed"]


def test_update_nonexistent_task(client: TestClient):
    update_data = {"title": "Updated Title", "description": "Updated Description"}
    response = client.put("/api/v1/tasks/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(client: TestClient):
    # Create a test task
    task_data = {"title": "Task to Delete", "description": "Will be deleted"}
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200

    # Verify task is deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task(client: TestClient):
    response = client.delete("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_task_invalid_data(client: TestClient):
    task_data = {"description": "Missing title field"}
    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 422


def test_pagination(client: TestClient):
    # Create 15 test tasks
    for i in range(15):
        task_data = {"title": f"Task {i}", "description": f"Description {i}"}
        client.post("/api/v1/tasks/", json=task_data)

    # Test default pagination (limit=100)
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 15

    # Test custom pagination
    response = client.get("/api/v1/tasks/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["title"] == "Task 5"


def test_create_task_with_priority(client: TestClient):
    task_data = {
        "title": "High Priority Task",
        "description": "Important task",
        "priority": "high",
        "completed": False,
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == Priority.HIGH


def test_create_task_with_due_date(client: TestClient):
    due_date = datetime.now() + timedelta(days=1)
    task_data = {
        "title": "Task with Due Date",
        "description": "Time-sensitive task",
        "due_date": due_date.isoformat(),
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert "due_date" in data
    assert datetime.fromisoformat(data["due_date"]).date() == due_date.date()


def test_create_recurring_task(client: TestClient):
    task_data = {
        "title": "Weekly Meeting",
        "description": "Team sync",
        "recurrence_type": "weekly",
        "recurrence_interval": 1,
        "due_date": datetime.now().isoformat(),
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["recurrence_type"] == RecurrenceType.WEEKLY
    assert data["recurrence_interval"] == 1
    assert "next_occurrence" in data


def test_create_task_with_category(client: TestClient, db_session):
    # Create a category first
    category = Category(name="Work")
    db_session.add(category)
    db_session.commit()

    task_data = {
        "title": "Work Task",
        "description": "Office related",
        "category_id": category.id,
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["category"]["name"] == "Work"


def test_create_task_with_tags(client: TestClient, db_session):
    # Create tags first
    tag1 = Tag(name="urgent")
    tag2 = Tag(name="project-x")
    db_session.add_all([tag1, tag2])
    db_session.commit()

    task_data = {
        "title": "Tagged Task",
        "description": "Task with multiple tags",
        "tag_ids": [tag1.id, tag2.id],
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 2
    tag_names = {tag["name"] for tag in data["tags"]}
    assert tag_names == {"urgent", "project-x"}


def test_update_task_priority(client: TestClient):
    # Create a task first
    task_data = {"title": "Original Priority", "priority": "low"}
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Update priority
    update_data = {"title": "Original Priority", "priority": "high"}
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == Priority.HIGH


def test_update_recurring_task(client: TestClient):
    # Create a recurring task
    task_data = {
        "title": "Original Recurrence",
        "recurrence_type": "weekly",
        "recurrence_interval": 1,
    }
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Update recurrence
    update_data = {
        "title": "Original Recurrence",
        "recurrence_type": "monthly",
        "recurrence_interval": 2,
    }
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["recurrence_type"] == RecurrenceType.MONTHLY
    assert data["recurrence_interval"] == 2
    assert "next_occurrence" in data


def test_filter_tasks_by_priority(client: TestClient):
    # Create tasks with different priorities
    priorities = ["low", "medium", "high"]
    for priority in priorities:
        task_data = {
            "title": f"{priority.capitalize()} Priority Task",
            "priority": priority,
        }
        client.post("/api/v1/tasks/", json=task_data)

    # Get all tasks and verify priorities
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    priority_counts = {Priority.LOW: 0, Priority.MEDIUM: 0, Priority.HIGH: 0}
    for task in data:
        priority_counts[task["priority"]] += 1
    assert priority_counts[Priority.LOW] == 1
    assert priority_counts[Priority.MEDIUM] == 1
    assert priority_counts[Priority.HIGH] == 1


def test_task_with_reminder(client: TestClient):
    reminder_date = datetime.now() + timedelta(hours=2)
    task_data = {
        "title": "Task with Reminder",
        "reminder_date": reminder_date.isoformat(),
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert "reminder_date" in data
    assert datetime.fromisoformat(data["reminder_date"]).date() == reminder_date.date()


def test_invalid_recurrence_type(client: TestClient):
    task_data = {
        "title": "Invalid Recurrence",
        "recurrence_type": "invalid_type",
        "recurrence_interval": 1,
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 422  # Validation error


def test_invalid_priority(client: TestClient):
    task_data = {"title": "Invalid Priority", "priority": "invalid_priority"}

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 422  # Validation error
