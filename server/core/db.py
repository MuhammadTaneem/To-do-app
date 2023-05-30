from sqlalchemy import create_engine, MetaData, orm
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5433/drafty", echo=True, future=True)
metadata_obj = MetaData()
metadata_obj.bind = engine
session_maker = orm.Session(engine)
mapper_registry = orm.registry()


# Base = declarative_base()


def create_session():
    return session_maker
# def mapper(mapped):
#     mapper_registry.map_imperatively(mapped)
