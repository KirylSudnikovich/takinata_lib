from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'sqlite:////home/snitch/PycharmProjects/VersionTwo/venv/lib/python3.5/site-packages/takinata_lib-0.1-py3.5.egg/database.sqlite3',
    echo=True)


class BugReport(Base):
    __tablename__ = 'bug_reports'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    description = Column(String)
    status = Column(Integer, default=1)


Base.metadata.create_all(engine)
