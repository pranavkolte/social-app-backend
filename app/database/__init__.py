from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from app.settings import settings


class Database:
    def __init__(self) -> None:
        self.engine = None
        self.Base = declarative_base()
        self.session = None

    def create_engine(self, echo=False):
        self.engine = create_engine(
            settings.DB_URI, echo=echo, poolclass=QueuePool
        )
        return self.engine

    def create_session(self):
        if not self.engine:
            raise Exception("Engine not initialized")
        Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        session = scoped_session(Session)
        self.session = session
        return session

    def create_tables(self):
        if not self.engine:
            raise Exception("Engine not initialized")
        self.Base.metadata.create_all(self.engine)

    def close_session(self):
        if self.session:
            self.session.close_all()

db = Database()
