from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import registry
from core import db
from .enum import TaskStatus
from sqlalchemy.sql import func

# mapper_registry = registry()

task_table = Table(
    "task", db.metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('author', Integer, ForeignKey('user.id')),
    Column('page_id', Integer, ForeignKey('page.id')),
    Column('task_name', String),
    Column('task_description', String),
    Column('status', String),
    Column('create_date', DateTime(timezone=True), server_default=func.now()),
    Column('last_edit', DateTime(timezone=True), onupdate=datetime.utcnow),
)

# db.metadata_obj.create_all(db.engine)


class Task:
    def __init__(self, status):
        self.status = status

    @property
    def status_label(self):
        return TaskStatus[self.status].value


task_mapper = registry().map_imperatively(Task, task_table)
