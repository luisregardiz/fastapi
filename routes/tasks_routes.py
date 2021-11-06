from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models.task_model import Task_schema, TaskCreate_schema, Tasks
from tortoise.contrib.fastapi import HTTPNotFoundError

from models.user_model import User_Pydantic
from utils.auth import get_current_user

tasks = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

class Status(BaseModel):
    message: str

# Get tasks
@tasks.get("/", response_model=List[Task_schema])
async def read_tasks(user: User_Pydantic = Depends(get_current_user)):
    tasks = await Tasks.filter(user_id=user.id).all()
    return tasks

@tasks.get("/{task_id}", response_model=Task_schema, responses={404: {"model": HTTPNotFoundError}})
async def read_task(task_id: int, user: User_Pydantic = Depends(get_current_user)):
    task = await Tasks.filter(user_id=user.id).get(id=task_id)
    return task

# Add task

@tasks.post("/", response_model=Task_schema)
async def create_task(task: TaskCreate_schema, user: User_Pydantic = Depends(get_current_user)):
    created_task = Tasks(title=task.title, task=task.task, is_completed=task.is_completed, user_id=user.id)
    await created_task.save()
    return await Task_schema.from_tortoise_orm(created_task)

# Update task

@tasks.put("/{task_id}", response_model=Task_schema, responses={404: {"model": HTTPNotFoundError}})
async def updating_task(task_id: int, task: TaskCreate_schema, user: User_Pydantic = Depends(get_current_user)):
    await Tasks.filter(user_id=user.id).filter(id=task_id).update(**task.dict(exclude_unset=True))
    task = await Tasks.get(id=task_id)
    return task

# Delete task
@tasks.delete("/{task_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def deleting_task(task_id: int, user: User_Pydantic = Depends(get_current_user)):
    deleted_task = await Tasks.filter(user_id=user.id).filter(id=task_id).delete()
    if not deleted_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return Status(message=f"Deleted task {task_id}")