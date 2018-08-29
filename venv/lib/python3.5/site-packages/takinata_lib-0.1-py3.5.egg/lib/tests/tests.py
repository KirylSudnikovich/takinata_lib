import unittest

from lib.controllers.user import *
from lib.controllers.project import *
from lib.controllers.category import *
from lib.exception import *


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
            UserController.delete(login)
        self.assertEqual(status, False)

    def test_user_delete(self):
        login = "test_user"
        password = "test_password"
        email = "test_email"

        try:
            UserController.reg(login, password, email)
            UserController.delete(login)
            status = True
        except IncorrentPassword:
            status = False

        self.assertEqual(status, True)

    def test_user_delete_no_user(self):
        login = "no_user"
        password = "password"

        try:
            UserController.delete(login)
            status = True
        except NoUser:
            status = False

        self.assertEqual(status, False)

class TestsProject(unittest.TestCase):

    def test_project_create_no_user(self):
        login = "test"
        password = "test"
        try:
            project = ProjectController.create(login, password, "test", "test")
            ProjectController.delete_by_id(login, password, project.id)
            status = True
        except NoUser or WrongPassword or ProjectWithThisNameAlreadyExist:
            status = False

        self.assertEqual(status, False)

    def test_project_create(self):
        login = "tester"
        password = "tester228"
        try:
            ProjectController.create(login, password, "test", "test")
            ProjectController.delete(login, password, "test")
            status = True
        except NoUser or WrongPassword or ProjectWithThisNameAlreadyExist:
            status = False

        self.assertEqual(status, True)

    def test_project_create_error(self):
        login = "test"
        password = "1"

        try:
            ProjectController.create(login, password, "test", "test")
            status = True
        except NoUser or WrongPassword:
            status = False

        self.assertEqual(status, False)

    def test_project_delete(self):
        login = "test"
        password = "test"
        try:
            ProjectController.create(login, password, "test", "test")
            ProjectController.delete(login, password, "test")
            status = True
        except NoUser or UAreNotAdmin:
            status = False

        self.assertEqual(status, False)

    def test_show_all(self):
        login = "test"
        password = "test"
        try:
            ProjectStorage.show_all_for_user(login, password)
            status = True
        except:
            status = False

        self.assertEqual(status, False)


class TestsCategory(unittest.TestCase):

    def test_column_create(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        c_name = "column_name"
        c_desc = "column_description"
        try:
            CategoryController.create_category(login, password, project_id, c_name, c_desc)
            CategoryController.delete_category(login, password, project_id, c_name)
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, True)

    # def test_column_create_error(self):
    #     login = "test"
    #     password = "test"
    #     name = "TestProject"
    #     c_name = "TestColumn"
    #     c_desc = ""
    #
    #     try:
    #         ColumnController.create_columm(login, password, name, c_name, c_desc)
    #         status = True
    #     except ColumnWithThisNameAlreadyExist:
    #         status = False
    #
    #     self.assertEqual(status, False)
    #
    # def test_column_delete(self):
    #     login = "test"
    #     password = "test"
    #     name = "TestProject"
    #     c_name = "column_name"
    #     c_desc = "column_description"
    #
    #     try:
    #         ColumnController.create_columm(login, password, name, c_name, c_desc)
    #         ColumnController.delete_column(login, password, name, c_name)
    #         status = True
    #     except:
    #         status = False
    #
    #     self.assertEqual(status, True)
    #
    # def test_column_show(self):
    #     login = "test"
    #     password = "test"
    #     name = "TestProject"
    #     c_name = "column_name"
    #     c_desc = "column_description"
    #
    #     try:
    #         ColumnController.create_columm(login, password, name, c_name, c_desc)
    #         ColumnController.show_all(login, password, name)
    #         ColumnController.delete_column(login, password, name, c_name)
    #         status = True
    #     except:
    #         status = False
    #
    #     self.assertEqual(status, True)
    #
    # def test_column_edit(self):
    #     login = "test"
    #     password = "test"
    #     project = "TestProject"
    #     column = "TestColumn"
    #
    #     try:
    #         ColumnController.edit_desc(login, password, project, column, "test")
    #         status = True
    #     except:
    #         status = False
    #
    #     self.assertEqual(status, True)



if __name__ == '__main__':
    unittest.main()
