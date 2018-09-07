import lib.logger as logger
from lib.models.models import User
from lib.storage.user import UserStorage
from lib.exception import UserAlreadyExist, NoUser, WrongPassword


class UserController:
    """
    The data handler for user. Allows to reg/delete or get user(s) or they information.

    """

    log_tag = "UserController"
    log = logger.get_logger(log_tag)

    @classmethod
    def reg(cls, username, password, email):
        """
        User registration with the specified data
        :param username: desired user name
        :param password: desired password
        :param email: desired e-mail
        :return: None. User will be added to database
        """
        user = User(username=username, password=password, email=email)
        users = UserStorage.get_all_users()
        have = False
        for i in users:
            if i.username == user.username or i.email == user.email:
                have = True
        if not have:
            UserStorage.add_user_to_db(user)
            UserController.log.info("User {} was successfully created in database".format(username))
            return user
        else:
            UserController.log.error(
                "Error. User with name {} can't be registred. User with this name/email is already registed".format(username))
            raise UserAlreadyExist

    @classmethod
    def delete(cls, username, password):
        """
        Delete user with the specified username from database
        :param username: username to delete
        :return: None. User will be deleted from database
        """
        user = UserStorage.get_user_by_name(username)
        if user != None:
            if user.password == password:
                UserStorage.delete_user_from_db(user)
                UserController.log.info("User {} was successfully deleted from database".format(username))
            else:
                UserController.log.error("Error. There is no user with username {}".format(username))
                raise WrongPassword
        else:
            raise NoUser

    @classmethod
    def get_user_by_name(cls, name):
        """
        Return 'user' object with that have specified name
        :param name: name of user to return
        :return: User object
        """
        user = UserStorage.get_user_by_name(name)
        if user != None:
            return user
        else:
            UserController.log.error("There is no user with '{}' username".format(name))
            raise NoUser

    @classmethod
    def get_user_by_id(cls, id):
        """
        Return 'user' object that have specified id
        :param id:
        :return: User object
        """
        user = UserStorage.get_user_by_id(id)
        if user != None:
            return user
        else:
            UserController.log.error("There is no user with {} id".format(id))
            raise NoUser

    @classmethod
    def get_all_users(cls):
        """
        Returned all 'user' objects from database
        :return:
        """
        users = UserStorage.get_all_users()
        if users != None:
            UserController.log.info("All users was returned from the database")
            return users
        else:
            UserController.log.error("There is no users in database")
            raise NoUser