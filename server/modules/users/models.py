from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import backref, relationship
from core.db import mapper_registry

# mapper_registry = registry()

user_table = Table(
    "user", mapper_registry.metadata,
    # "user", mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('password', String),
    Column('address', String),
    Column('email', String),
    Column('active', Boolean, default=False)
)

user_token_table = Table(
    "user_token",  mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('author', Integer, ForeignKey('user.id', ondelete='CASCADE')),
    Column('token', String),
    Column('expire', DateTime),
    Column('used', Boolean, default=False)
)


class UserToken:
    pass


class User:
    pass
    # reset_token = relation(UserReset, back_populates='user')


user_mapper = mapper_registry.map_imperatively(User, user_table)

user_password_reset_mapper = mapper_registry.map_imperatively(UserToken, user_token_table, properties={
    'user': relationship(User,  backref=backref('token'), lazy='joined', uselist=False),
})