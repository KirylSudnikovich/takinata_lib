from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracker.models import BugReport
from lib.conf import get_path_to_db
from lib.models.models import User, Project, Category, Task

engine = create_engine(get_path_to_db())
Session = sessionmaker(bind=engine)
session = Session()


class BugController:
    @classmethod
    def add_bug(cls, username, name, description):
        bug = BugReport(username=username, name=name, description=description)
        session.add(bug)
        session.commit()
        session.close()

    @classmethod
    def get_all_bugs(cls):
        bugs = session.query(BugReport).all()
        session.close()
        return bugs


def all_users():
    user = session.query(User).order_by(User.id.desc()).first()
    session.close()
    if user is None:
        return 0
    return user.id


def all_projects():
    project = session.query(Project).order_by(Project.id.desc()).first()
    if project is None:
        return 0
    session.close()
    return project.id


def all_categories():
    category = session.query(Category).order_by(Category.id.desc()).first()
    if category is None:
        return 0
    session.close()
    return category.id


def all_tasks():
    task = session.query(Task).order_by(Task.id.desc()).first()
    if task is None:
        return 0
    session.close()
    return task.id
