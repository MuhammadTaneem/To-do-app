from datetime import date
from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    page_id: int
    task_name: str
    task_description: str | None
    status: str

    class Config:
        orm_mode = True


class ReadTask(Task):
    id: int
    create_date: Optional[date]
    last_edit: Optional[date]

    class Config:
        orm_mode = True


class SingleTaskList(BaseModel):
    id: int
    task_name: str

    class Config:
        orm_mode = True


class TaskListView(BaseModel):
    tasks: list[SingleTaskList]
