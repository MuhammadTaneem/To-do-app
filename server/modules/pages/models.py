from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import registry
from core.db import mapper_registry
from sqlalchemy.sql import func

from modules.pages.tasks.models import task_table

page_table = Table(
    "page", mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    # Column('author', Integer, ForeignKey('user.id')),
    Column('author', Integer, ForeignKey('user.id', ondelete='CASCADE')),
    Column('parent_page_id', Integer, default=0),
    Column('page_name', String, default="Unnamed"),
    Column('page_description', String),
    Column('color', String),
    Column('create_date', DateTime(timezone=True), server_default=func.now()),
    Column('last_edit', DateTime(timezone=True), onupdate=datetime.utcnow),

    # ForeignKeyConstraint(
    #         ['parent_page_id'], ['page.id'], ondelete='CASCADE',
    #         deferrable=True, initially='DEFERRED'
    #     ),
)




# Define the foreign key relationship explicitly
# page_table.append_constraint(
#     ForeignKeyConstraint(
#         ['id'], [task_table.c.page_id], ondelete='CASCADE',
#         deferrable=True, initially='DEFERRED'
#     )
# )


# db.metadata_obj.create_all(db.engine)


class Page:
    pass


page_mapper = registry().map_imperatively(Page, page_table)
