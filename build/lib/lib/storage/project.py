import sqlite3
import lib.conf as conf
import copy
from lib.exception import *
from lib.models.project import *
from lib.models.models import *
from lib.storage.user import UserStorage
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
engine = create_engine(conf.get_path_to_db())
from sqlalchemy.ext.declarative import declarative_base

class ProjectStorage:
    @classmethod
    def add_project_to_db(cls, project, user):
        """
        Add an instance of the Project class to the database
        :param project: the instance of the Project class that you want to add
        :param user: an instance of the User class that is the Creator of the project
        :return:
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        all_projectnames = session.query(Project).all()
        yep = False
        for i in all_projectnames:
            if project.name == i.name and user.id == i.user_id:
                yep = True
        if not yep:
            session.add(project)
            session.commit()
            session.close()
        else:
            raise ProjectWithThisNameAlreadyExist()

    @classmethod
    def get_all_persons_in_project(cls, project):
        Session = sessionmaker(bind=engine)
        session = Session()
        pr = session.query(Project).filter(Project.name==project.name).first()
        to_send = pr.users
        session.close()
        return to_send

    @classmethod
    def get_all_persons_in_project_by_id(cls, project):
        Session = sessionmaker(bind=engine)
        session = Session()
        pr = session.query(Project).filter(Project.id == project.id).first()
        to_send = pr.users
        session.close()
        return to_send

    @classmethod
    def add_person_to_project(cls, person, project):
        """
        Adds the specified user to the project if the command was executed on behalf of the project creator
        :param person: person to add to the project
        :param project: project where you want to add the user
        :return:
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        new_project = session.query(Project).filter(Project.id == project.id).first()
        new_project.users.append(person)
        session.commit()
        session.close()
        return project

    @classmethod
    def delete_person_from_project(cls, person, project):
        """
        Remove the specified user from the project
        :param person: person to remove
        :param project: project where you want to remove the user
        :return:
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        new_project = session.query(Project).filter(Project.id == project.id).first()
        delUser = None
        for user in new_project.users:
            if user.id == person.id:
                delUser = user
        new_project.users.remove(delUser)
        session.commit()
        session.close()

    @classmethod
    def delete_with_object(cls, project):
        """
        Delete the specified project that was passed in the arguments
        :param project: project whitch you want to delete
        :return:
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        session.delete(project)
        session.commit()
        session.close()

    @classmethod
    def get_project(cls, name):
        """
        Getting the project with the specified name from the database
        :param name: name of the project
        :return: project
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        project = session.query(Project).filter(Project.name==name).first()
        session.close()
        return project

    @classmethod
    def get_project_by_id(cls, pid):
        """
        Getting the project with the specified name from the database
        :param name: name of the project
        :return: project
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        project = session.query(Project).filter(Project.id==pid).first()
        session.close()
        return project


    @classmethod
    def show_all(cls):
        """
        Displays a list of all projects in which the specified user is involved
        :return: project list
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        projects = session.query(Project).all()
        session.close()
        return projects

    @classmethod
    def check_permission(cls, person, project):
        """
        Checks whether the specified user is participating in the project
        :param person: the supposed worker
        :param project: project to check
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        guys = ProjectStorage.get_all_persons_in_project_by_id(project)
        for i in guys:
            print(i.id)
            if i.id == person.id:
                return
        raise NoPermission

    @classmethod
    def is_admin(cls, person, project):
        """
        Checks whether the specified user is the creator of the project
        :param person: the supposed creator
        :param project: project to check
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        guys = ProjectStorage.get_all_persons_in_project_by_id(project)
        if guys[0].id == person.id:
            return 0
        else:
            raise UAreNotAdmin

    @classmethod
    def save(self, project):
        """
        Saves the transferred instance of the Project class to the database
        :param project: project to save
        :return:
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        new_project = session.query(Project).filter(Project.id == project.id).first()
        new_project.name = project.name
        new_project.description = project.description
        session.commit()
        session.close()