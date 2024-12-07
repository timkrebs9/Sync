from sqlalchemy.orm import Session

from app.models.task_model import Tag, Task
from app.schemas.task_schema import TaskCreate
from app.services.task_service import calculate_next_occurrence


def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump(exclude={"tag_ids"}))

    if task.tag_ids:
        db_task.tags = db.query(Tag).filter(Tag.id.in_(task.tag_ids)).all()

    if db_task.recurrence_type:
        db_task.next_occurrence = calculate_next_occurrence(db_task)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return None

    for key, value in task.model_dump(exclude={"tag_ids"}).items():
        setattr(db_task, key, value)

    if task.tag_ids is not None:
        db_task.tags = db.query(Tag).filter(Tag.id.in_(task.tag_ids)).all()

    if db_task.recurrence_type:
        db_task.next_occurrence = calculate_next_occurrence(db_task)

    db.commit()
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return None  # or raise HTTPException
    db.delete(db_task)
    db.commit()
    return db_task
