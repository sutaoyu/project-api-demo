from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, ValidationError, validator
from enum import Enum

from app.schemas.base import QueryBase


class TaskType(str, Enum):
    daily = "daily"
    meeting = "meeting"
    area = "area"


class TaskStatus(int, Enum):
    runing = 0
    finished = 1


class TaskQueryStatus(int, Enum):
    all = -1
    runing = 0
    finished = 1


class TaskQuery(QueryBase):
    type: Optional[TaskType] = None
    status: Optional[TaskQueryStatus] = -1
    # 在task_name,source,description中匹配关键词
    keywords: Optional[str] = ""


# Shared properties
class TaskBase(BaseModel):
    task_name: str
    source: str
    type: TaskType
    description: Optional[str] = None
    responsible_user_id: Optional[str] = None
    start_time: datetime
    end_time: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


# Properties to receive on task creation
class TaskCreate(TaskBase):
    pass


# Properties to receive on task update
class TaskUpdate(TaskBase):
    pass


# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    task_id: str
    status: TaskStatus
    owner_user_id: str
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class TaskInDB(TaskInDBBase):
    id: int


# Properties to return to client
class Task(TaskInDBBase):
    pass
