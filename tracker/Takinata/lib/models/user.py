class User:
    """
    An entity of type user. Contains the user name, password, and e-mail fields. Is the identifier by which it is
    determined who owns a particular project or task
    """
    def __init__(self, username, password, email, user_id=None):
        self.username = username
        self.password = password
        self.email = email
        self.user_id = user_id

    def __str__(self):
        return self.username
