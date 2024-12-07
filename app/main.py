from fastapi import FastAPI
from app.api.v1.endpoints import tasks
from app.core.database import engine
from app.models import task_model

task_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Snyc API",
    description="Task Management API for Snyc iOS Application",
    version="1.0.0"
)

app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])

