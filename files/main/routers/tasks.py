from fastapi import APIRouter, Depends, HTTPException, status

from files.main.schemas.schemas import TaskCreate, TaskSchema, TaskUpdate
from files.main.services.services import TaskNotFound, TaskService

router=APIRouter(prefix='/tasks')# создаем связь между входом в приложение
from files.main.routers.dependencies import get_task_services


@router.get('')
def Read_Tasks(task_service: TaskService=Depends(get_task_services))->list[TaskSchema]:
    return task_service.list_tasks()
@router.post('',status_code=status.HTTP_201_CREATED)
def get_task(payload: TaskCreate, task_service: TaskService=Depends(get_task_services))->TaskSchema:
        return task_service.create_task(task_create=payload)
@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def Delete_Task(task_id: str, task_service=Depends(get_task_services))-> None:
    try:
        task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
@router.patch('/{task_id}')
def Update_Task(payload:TaskUpdate ,task_id: str,  task_service=Depends(get_task_services)):
    try:
        return task_service.update_task(task_id=task_id,task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)