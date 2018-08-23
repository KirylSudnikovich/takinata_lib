import os

import lib.logger as logger
from lib.models.models import User, create_tables
from lib.storage.user import UserStorage
from lib.storage.project import ProjectStorage
from lib.exception import *
import lib.conf as conf


class UserController:
    log_tag = "UserController"

    create_tables()

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
        #user = LibUser.create(username=username, password=password, email=email)
        user = User(username=username, password=password, email=email)
        users = UserStorage.get_all_users()
        have = False
        for i in users:
            if i.username == user.username:
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
