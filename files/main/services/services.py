from sqlalchemy.orm import Session

from files.main.repositories.repositories import TaskRepos
from files.main.schemas.schemas import TaskCreate, TaskSchema, TaskUpdate


class TaskNotFound(Exception):
    '''Задача не найдена в БД'''
class TaskService:
    def __init__(self,db: Session):
        self.db=db
        self.task_repository = TaskRepos(db)
    def list_tasks(self)->list[TaskSchema]:
        task_orm=self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in task_orm]
    def create_task(self,task_create: TaskCreate)->TaskSchema:
        task_orm=self.task_repository.create(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdate) -> TaskSchema:
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if task_for_update is None:
            raise TaskNotFound(f"Задача {task_id} не найдена в бд")
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete=self.task_repository.get_by_id(task_id=task_id)
        if task_for_delete is None:
            raise TaskNotFound(f"Задача {task_id} не найдена в бд")
        self.task_repository.delete(task_for_delete)
        self.db.commit()

