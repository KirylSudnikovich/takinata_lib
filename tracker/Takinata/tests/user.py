import unittest

from Tracker.lib.controllers.User import *
from Tracker.lib.Exception import *


# научиться запускать тесты одной командой
class TestsUser(unittest.TestCase):

    def test_user_registration(self):
        login = "test_user"
        password = "test_password"
        email = "test_email"

        try:
            user = UserController.reg(login, password, email)
            status = True
            UserController.delete(login, password)
        except:
            status = False
            UserController.delete(login, password)
        self.assertEqual(status, False)

    def test_user_delete(self):
        login = "test_user"
        password = "test_password"
        email = "test_email"

        try:
            UserController.reg(login, password, email)
            UserController.delete(login, password)
            status = True
        except IncorrentPassword:
            status = False

        self.assertEqual(status, True)

    def test_user_delete_no_user(self):
        login = "no_user"
        password = "password"

        try:
            UserController.delete(login, password)
            status = True
        except NoUser:
            status = False

        self.assertEqual(status, False)

    def test_user_delete_incorrect_password(self):
        login = "test_user"
        password = "test_password"
        email = "test_email"
        UserController.reg(login, password, email)

        try:
            UserController.delete(login, 1)
            status = True
        except IncorrentPassword:
            UserController.delete(login, password)
            status = False

        self.assertEqual(status, False)

    def test_user_edit(self):
        login = "test_user"
        password = "test_password"
        email = "test_email"

        UserController.reg(login, password, email)

        try:
            UserController.edit(login, password, password, 5)
            status = True
        except IncorrentPassword:
            status = False

        self.assertEqual(status, True)


if __name__ == '__main__':
    unittest.main()
