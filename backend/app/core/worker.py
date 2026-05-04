from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.autodiscover_tasks(["app.tasks"])

import app.tasks.evaluation_tasks