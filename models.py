import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine
from datetime import datetime, timezone
class Status(enum.Enum):
    incomplete = "incomplete"
    complete = "complete"

class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(Status), default=Status.incomplete)
    priority = Column(Enum(Priority), default=Priority.medium)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    #owner = relationship("User", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="tasks_assigned")
    creator = relationship("User", foreign_keys=[created_by])

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    #tasks = relationship("Task", back_populates="owner")
    tasks_assigned = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")

Base.metadata.create_all(engine)