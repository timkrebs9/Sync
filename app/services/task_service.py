from datetime import datetime, timedelta
from app.models import RecurrenceType, Task


def calculate_next_occurrence(task: Task) -> datetime:
    if not task.recurrence_type or not task.recurrence_interval:
        return datetime.now()

    base_date = task.next_occurrence or task.due_date or datetime.now()

    if task.recurrence_type == RecurrenceType.DAILY:
        return base_date + timedelta(days=task.recurrence_interval)
    elif task.recurrence_type == RecurrenceType.WEEKLY:
        return base_date + timedelta(weeks=task.recurrence_interval)
    elif task.recurrence_type == RecurrenceType.MONTHLY:
        # Add months (simplified)
        return base_date + timedelta(days=30 * task.recurrence_interval)
    elif task.recurrence_type == RecurrenceType.YEARLY:
        # Add years (simplified)
        return base_date + timedelta(days=365 * task.recurrence_interval)

    return datetime.now()
