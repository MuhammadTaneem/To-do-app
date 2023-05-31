from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import registry
from core.db import mapper_registry
from sqlalchemy.sql import func

# mapper_registry = registry()

page_table = Table(
    "page", mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('author', Integer, ForeignKey('user.id')),
    Column('parent_page_id', Integer, default=0),
    Column('page_name', String),
    Column('page_description', String),
    Column('color', String),
    Column('create_date', DateTime(timezone=True), server_default=func.now()),
    Column('last_edit', DateTime(timezone=True), onupdate=datetime.utcnow),
)

# db.metadata_obj.create_all(db.engine)


class Page:
    pass
    # def __repr__(self) -> str:
    #     return self.page_name


page_mapper = registry().map_imperatively(Page, page_table)
