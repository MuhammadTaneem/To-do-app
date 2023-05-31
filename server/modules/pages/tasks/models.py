from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import registry
from core.db import mapper_registry
from .enum import TaskStatus
from sqlalchemy.sql import func

task_table = Table(
    "task", mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('author', Integer, ForeignKey('user.id')),
    Column('page_id', Integer, ForeignKey('page.id')),
    Column('task_name', String),
    Column('task_description', String),
    Column('status', String),
    Column('create_date', DateTime(timezone=True), server_default=func.now()),
    Column('last_edit', DateTime(timezone=True), onupdate=datetime.utcnow),
)



class Task:
    @hybrid_property
    def status_label(self):
        return TaskStatus[self.status].value


task_mapper = registry().map_imperatively(Task, task_table)
