from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from .. import Base


class BaseRepository:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.create_tables()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
