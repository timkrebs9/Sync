from fastapi import FastAPI
from app.core.middleware import SubscriptionMiddleware
from app.core.security_middleware import RateLimitMiddleware
from app.api.v1.endpoints import tasks
from app.api.v2.endpoints import auth, tasks as tasks_v2
from app.core.database import engine
from app.models import task_model, user_model

task_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Snyc API",
    description="Task Management API for Snyc iOS Application",
    version="2.0.0",
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(SubscriptionMiddleware)

app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks-free"])
app.include_router(auth.router, prefix="/api/v2/auth", tags=["authentication"])
app.include_router(tasks_v2.router, prefix="/api/v2/tasks", tags=["tasks-premium"])
