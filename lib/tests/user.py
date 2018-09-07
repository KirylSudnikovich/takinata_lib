import unittest
from lib.controllers.user import *


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
        self.assertEqual(status, True)

    def test_user_reg_already_username(self):
        login = "tester"
        password = "test_password"
        email = "test_email"
        try:
            user = UserController.reg(login, password, email)
            status = True
        except:
            status = False
        self.assertEqual(status, False)

    def test_user_reg_already_email(self):
        login = "tester"
        password = "test_password"
        email = "test@tester.com"
        try:
            user = UserController.reg(login, password, email)
            status = True
        except:
            status = False
        self.assertEqual(status, False)

    def test_user_delete(self):
        login = "test_user"
        password = "test_password"
        email = "test_email"
        try:
            UserController.reg(login, password, email)
            UserController.delete(login, password)
            status = True
        except WrongPassword:
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

    def test_get_user_by_name(self):
        login = "tester"
        try:
            UserController.get_user_by_name(login)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_user_by_name_nouser(self):
        login = "adm1n"
        try:
            UserController.get_user_by_name(login)
            status = True
        except NoUser:
            status = False
        self.assertEquals(status, False)

    def test_get_user_by_id(self):
        id = 8
        try:
            UserController.get_user_by_id(8)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_user_by_no_id(self):
        id = -1000
        try:
            UserController.get_user_by_id(id)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_all_users(self):
        try:
            UserController.get_all_users()
            status = True
        except:
            status = False
        self.assertEquals(status, True)
