import unittest

from Tracker.lib.controllers.Project import *
from Tracker.lib.Exception import *


class TestsProject(unittest.TestCase):

    def test_project_create(self):
        login = "test"
        password = "test"

        try:
            ProjectController.create(login, password, "test", "test")
            ProjectController.delete(login, password, "test")
            status = True
        except NoUser or IncorrentPassword or ProjectWithThisNameAlreadyExist:
            status = False

        self.assertEqual(status, True)

    def test_project_create_eror(self):
        login = "test"
        password = "1"

        try:
            ProjectController.create(login, password, "test", "test")
            status = True
        except IncorrentPassword:
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

        self.assertEqual(status, True)

    def test_show_all(self):
        login = "test"
        password = "test"
        try:
            ProjectController.show_all(login, password)
            status = True
        except:
            status = False

        self.assertEqual(status, True)

    def test_edit_name(self):
        login = "test"
        password = "test"
        name = "TestProject"
        try:
            ProjectController.edit_name(login, password, name, name)
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, True)

    def test_edit_desc(self):
        login = "test"
        password = "test"
        name = "TestProject"
        try:
            ProjectController.edit_description(login, password, name, "test")
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, True)


if __name__ == '__main__':
    unittest.main()
