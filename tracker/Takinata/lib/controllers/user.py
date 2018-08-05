import os

import lib.logger as logger
from lib.models.user import User
from lib.storage.user import UserStorage
from lib.exception import *
import lib.conf as conf


def create_table():
    UserStorage.create_table()

def check_tracker_folder(path):
    """
    Checks for a directory at the specified path. If the directory does not exist, it will be created
    :param path: path to check
    :return:
    """
    if not os.path.exists(path):
        f = open(path, 'w')
        f.close()
        print("all clear")
        return 1


def check_db_exists(path):
    """
    Checks if the database exists in the specified directory. If not - creates this base
    :param path: path to database
    :return:
    """
    if check_tracker_folder(path) == 1:
        create_table()
        return 0


class UserController:
    log_tag = "UserController"

    check_db_exists(conf.get_path_to_db())

    @classmethod
    def reg(cls, username, password, email):
        """
        User registration with the specified data
        :param username: desired user name
        :param password: desired password
        :param email: desired e-mail
        :return:
        """
        log = logger.get_logger(UserController.log_tag)
        user = User(username, password, email)
        users = UserStorage.get_all_users()
        have = False
        for i in users:
            if i[0] == user.username:
                have = True
        if not have:
            UserStorage.add_user_to_db(user)
            return user
        else:
            log.error("User with this name is already exist")
            raise UserAlreadyExist

    @classmethod
    def edit(cls, username, password, param, newparam):
        """
        Editing user information
        :param username: name of user
        :param password: password
        :param param: param you want to change (name/password)
        :param newparam: new value of param
        :return:
        """
        log = logger.get_logger(UserController.log_tag)
        user = UserStorage.get_user_by_name(username)
        oldname = user.username
        if user.password == password:
            if param == 'name':
                user.username = newparam
                UserStorage.set_username_for_user(user, oldname)
            elif param == 'password':
                user.password = newparam
                UserStorage.set_password_for_user(user)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def delete(cls, username, password):
        """
        Function to delete a user
        :param username: username of user to delete
        :param password: him password
        :return:
        """
        log = logger.get_logger(UserController.log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            UserStorage.delete_user(username)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword
