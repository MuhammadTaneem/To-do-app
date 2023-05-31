from sqlalchemy import create_engine, MetaData, orm

engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5433/drafty", echo=True)
metadata_obj = MetaData()
metadata_obj.bind = engine
session_maker = orm.Session(engine)
mapper_registry = orm.registry()


class SessionManager:
    _session = None

    @staticmethod
    def create_session():
        if SessionManager._session is None:
            SessionManager._session = session_maker
        return SessionManager._session
