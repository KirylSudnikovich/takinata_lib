from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine, Date, Time, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from lib.conf import get_path_to_db
Base = declarative_base()

engine = create_engine(get_path_to_db())


rel = Table('user_project', Base.metadata,
            Column('user_id', Integer, ForeignKey('users.id')),
            Column('project_id', Integer, ForeignKey('projects.id')))

class Task(Base):
    """
    Task
    A task is some action that you want to do in the future.

    name - name of task. It must be unique within on category
    desc - a description that should reflect the essence of that the task need to done. Can be empty
    start_date - the date the task was started. It can not be earlier than 01/01/2018. Optional field
    start_time - the time the task was started. Optional field
    end_date - the date that task will be done. Optional field
    end_time - the time the task will be done. Optional field
    priority - priority of the task. There may be [max, medium, min]
    is_archive - shows the status of the task at this time. 0 - in progress, 1 - complete
    is_subtask - whether this task is a subtask. 1 - is. If the task is a subtask, the id of the parent task will be specified in the parent_task_id field
    parent_task_id - id of the parent task. It is important if the task is a subtask
    assosiated_task_id - if the task is associated with another task, the field contains the idi of the task with which the task is associated
    type - type of task. 1 - one time, 2 - regular
    period - if the task is periodic, this field contains the period of this task in days
    user_id - the user who created the task
    category_id - category to which the given task belongs
    project_id - the project to which this task belongs
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    start_date = Column(String)
    start_time = Column(String)
    end_date = Column(String)
    end_time = Column(String)
    priority = Column(String)
    is_archive = Column(Integer)
    is_subtask = Column(Integer)
    parent_task_id = Column(Integer)
    is_parent = Column(Integer)
    assosiated_task_id = Column(Integer)
    type = Column(Integer)
    period = Column(Integer)
    to_deadline = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))



class Category(Base):
    """
    Category
    A category is a set of tasks grouped by one topic or area.

    name - name of category. It must be unique within one project
    desc - a description that should reflect the essence of what the category contains. Can be empty
    project_id - project id to which this category belongs
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class User(Base):
    """
    User - user of the library. It’s impossible to interact with the library without the user

    username - user name, can use as login
    password - user password
    email - user email (no email activation)
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)

class Project(Base):
    """
    Project
    A project is an abstraction that will contain categories that in turn contain your tasks.

    name - the name of the project to be displayed in the project list. The name must be unique for each user. That is, two projects for one user will not be created, and for different projects will be created
    description - the description of the project, which should reflect its essence. Can be empty
    user_id - id of the user who created the project
    users - list (array) of all users participating in this project
    """

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