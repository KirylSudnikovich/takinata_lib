from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from lib.conf import conf

Base = declarative_base()

engine = create_engine(conf.get_path_to_db())


class BugReport(Base):
    __tablename__ = 'bug_reports'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    description = Column(String)
    status = Column(Integer, default=1)


Base.metadata.create_all(engine)
