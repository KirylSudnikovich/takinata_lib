from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine, Date, Time, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
Base = declarative_base()
engine = create_engine('sqlite:////home/snitch/PycharmProjects/VersionTwo/venv/lib/python3.5/site-packages/takinata_lib-0.1-py3.5.egg/database.sqlite3', echo=True)

rel = Table('user_project', Base.metadata,
            Column('user_id', Integer, ForeignKey('users.id')),
            Column('project_id', Integer, ForeignKey('projects.id')))

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    start_date = Column(String)
    start_time = Column(String)
    end_date = Column(String)
    end_time = Column(String)
    tags = Column(Text)
    priority = Column(Integer)
    is_archive = Column(Integer)
    is_subtask = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    #projects = relationship('Project', secondary=rel, backref='users')

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(String)
    users = relationship('User', secondary=rel, backref='projects')
    columns = relationship('Category')


Base.metadata.create_all(engine)

def create_tables():
    Base.metadata.create_all(engine)