import sqlite3

from lib import conf
from lib.exception import *
from lib.models.project import *
from lib.models.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine(conf.get_path_to_db())
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserStorage:
    @classmethod
    def add_user_to_db(cls, user):
        """
        Add the transferred user to the database
        :param user: user to add
        :return:
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(user)
        session.commit()
        session.close()
        return

    @classmethod
    def get_all_users(cls):
        """
        Get a list of names of all existing users
        :return: list of user names
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        users = session.query(User).all()
        session.close()
        return users

    @classmethod
    def right_get_all_users(cls):
        """
        Get a list of names of all existing users
        :return: list of user names
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        data = c.fetchall()
        #print(data)
        user_list = []
        for i in data:
            user = User(i[1],i[2],i[3],i[0])
            user_list.append(user)
        conn.close()
        return user_list

    @classmethod
    def get_project(cls, name):
        """
        Getting the project by the specified name
        :param name: name of project
        :return: project
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE name==('%s')" % name)
        data = c.fetchone()
        conn.close()
        project = Project(data[1], data[2], data[3], None, data[0])
        return project

    @classmethod
    def get_user_by_name(cls, name):
        """
        Get the user by the specified name
        :param name: user name
        :return:
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter(User.username==name).first()
        print(user)
        session.close()
        return user

    @classmethod
    def get_user_by_id(cls, id):
        """
        Get the user by the specified id
        :param id: user id
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id==('%s')" % id)
        data = c.fetchone()
        if data is None:
            return NoUser
        else:
            user = User(data[1], data[2], data[3], data[0])
            return user

    @classmethod
    def delete_user(cls, name):
        """
        Remove the user with the specified name from the database
        :param name:
        :return:
        """
        user = UserStorage.get_user_by_name(name)
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username==('%s')" % user.username)
        conn.commit()
        conn.close()

    @classmethod
    def get_password_for_user(cls, username):
        """
        Get the password for the specified user
        :param username: user name
        :return: password
        """
        try:
            conn = sqlite3.connect(conf.get_path_to_db())
            c = conn.cursor()
            c.execute("SELECT id, password FROM users WHERE username==('%s') " % username)
            data = c.fetchone()
            return data[1]
        except:
            return 1

    @classmethod
    def set_password_for_user(cls, user):
        """
        Setting a password for the user
        :param user: user object
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE users SET password=('%s') WHERE username==('%s')" % (user.password, user.username))
        conn.commit()
        conn.close()

    @classmethod
    def set_username_for_user(cls, user, oldname):
        """
        Setting a new username for the user
        :param user: user object
        :param oldname: old name of user
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE users SET username=('%s') WHERE username==('%s')" % (user.username, oldname))
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        path = conf.get_path_to_db()
        print("__________________________")
        print(path)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("CREATE TABLE `users` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `username`	TEXT, `password` TEXT, "
                  "`email` TEXT);")
        conn.commit()
        conn.close()