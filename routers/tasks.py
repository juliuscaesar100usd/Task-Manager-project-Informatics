from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import User, Task
from schemas import TaskCreate, TaskResponse, TaskUpdate
from dependencies import get_current_user, require_admin

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@tasks_router.post("/", response_model=TaskResponse)

def create_task(task_data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_user = db.query(User).filter(User.id == task_data.assigned_to).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")
    else:
        new_task = Task(title=task_data.title, description=task_data.description, assigned_to=task_data.assigned_to, status=task_data.status, created_by=current_user.id, priority=task_data.priority, deadline=task_data.deadline)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return TaskResponse.model_validate(new_task)
    
@tasks_router.get("/", response_model=list[TaskResponse])

def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    tasks = db.query(Task).all()
    return [TaskResponse.model_validate(task) for task in tasks]

@my_tasks_router.get("/", response_model=list[TaskResponse])

def get_my_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.assigned_to == current_user.id).all()
    return [TaskResponse.model_validate(task) for task in tasks]

@my_tasks_router.get("/{task_id}", response_model=TaskResponse)

def get_my_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.assigned_to == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    elif task.assigned_to != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
    else:
        return TaskResponse.model_validate(task)

@tasks_router.get("/{task_id}", response_model=TaskResponse)

def get_one_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse.model_validate(task)

@tasks_router.put("/{task_id}", response_model=TaskResponse)

def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    else:
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return TaskResponse.model_validate(task)
    
@tasks_router.delete("/{task_id}", status_code=status.HTTP_200_OK)

def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    else:
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}