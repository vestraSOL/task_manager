from fastapi import Depends
from sqlalchemy.orm import Session

from files.main.db.session import get_db
from files.main.services.services import TaskService


def get_task_services(db: Session=Depends(get_db)):
    return TaskService(db)

