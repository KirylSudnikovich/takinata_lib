class MainException(Exception):
    pass


class UserAlreadyExist(UserException):
    def __init__(self):
        super().__init__("A user with this name is already registered")