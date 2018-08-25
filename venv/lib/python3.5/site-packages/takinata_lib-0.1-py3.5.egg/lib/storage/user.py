import sqlite3

from lib import conf
from lib.exception import *
from lib.models.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(conf.get_path_to_db())
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class UserStorage:
    """
    UserStorage class. Allow to add/delete user from database or get by name/id

    """

    @classmethod
    def add_user_to_db(cls, user):
        """
        Add the transferred user to the database
        :param user: user to add
        :return: None. User was added to database
        """
        session.add(user)
        session.commit()
        session.close()

    @classmethod
    def delete_user_from_db(cls, user):
        """
        Delete the transferred user from the database
        :param user: user to delete
        :return: None. User was removed from database
        """
        user = session.query(User).filter(User.id == user.id).first()
        session.delete(user)
        session.commit()
        session.close()

    @classmethod
    def get_all_users(cls):
        """
        Return 'list' with all users that database have
        :return:  List of 'user' objects
        """
        users = session.query(User).all()
        session.close()
        return users

    @classmethod
    def get_user_by_name(cls, name):
        """
        Get the user by the specified name
        :param name: user name
        :return: 'User' object
        """
        user = session.query(User).filter(User.username == name).first()
        session.close()
        return user

    @classmethod
    def get_user_by_id(cls, id):
        """
        Get the user by the specified id
        :param id: user id
        :return: 'User' object
        """
        user = session.query(User).filter(User.id == id).first()
        session.close()
        return user