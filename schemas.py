from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from models import Status, Priority
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[Status] = Status.incomplete
    priority: Optional[Priority] = Priority.medium
    deadline: datetime
    assigned_to: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    deadline: Optional[datetime] = None
    assigned_to: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Status
    priority: Priority
    deadline: Optional[datetime] = None
    created_at: datetime
    assigned_to: int
    created_by: int

    model_config = ConfigDict(from_attributes=True)