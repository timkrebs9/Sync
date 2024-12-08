from sqlalchemy.orm import Session
from app.models.task_model import Tag, Task
from app.models.user_model import User, UserRole
from app.schemas.task_schema import TaskCreate
from app.services.task_service import calculate_next_occurrence
from app.core.permissions import is_task_owner


def create_task(db: Session, task: TaskCreate, current_user: User):
    db_task = Task(**task.model_dump(exclude={"tag_ids"}))
    db_task.user_id = current_user.id

    if task.tag_ids:
        db_task.tags = db.query(Tag).filter(Tag.id.in_(task.tag_ids)).all()

    if db_task.recurrence_type:
        db_task.next_occurrence = calculate_next_occurrence(db_task)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, current_user: User, skip: int = 0, limit: int = 100):
    if current_user.role == UserRole.ADMIN:
        return db.query(Task).offset(skip).limit(limit).all()
    return db.query(Task).filter(Task.user_id == current_user.id).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int, current_user: User):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task and (is_task_owner(current_user, task.user_id) or current_user.role == UserRole.ADMIN):
        return task
    return None


def update_task(db: Session, task_id: int, task: TaskCreate, current_user: User):
    db_task = get_task(db, task_id=task_id, current_user=current_user)
    if db_task is None:
        return None

    task_data = task.model_dump(exclude={"tag_ids"})
    for key, value in task_data.items():
        setattr(db_task, key, value)

    if task.tag_ids:
        db_task.tags = db.query(Tag).filter(Tag.id.in_(task.tag_ids)).all()

    if db_task.recurrence_type:
        db_task.next_occurrence = calculate_next_occurrence(db_task)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, current_user: User):
    db_task = get_task(db, task_id=task_id, current_user=current_user)
    if db_task is None:
        return None

    db.delete(db_task)
    db.commit()
    return db_task
