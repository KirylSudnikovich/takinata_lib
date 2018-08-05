import unittest

from Tracker.lib.controllers.Task import *
from Tracker.lib.Exception import *


class TestsTask(unittest.TestCase):

    def test_task_add(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "20.10.2019"
        second_date = "25.10.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.delete_task(login, password, project, column, name)
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, True)

    def test_task_delete(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "20.10.2020"
        second_date = "25.10.2021"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.delete_task(login, password, project, column, name)
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, True)

    def test_task_show(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        try:
            TaskController.show_tasks(login, password, project, column)
            status = True
        except:
            status = False

        self.assertEqual(status, True)

    def test_task_create_before_now(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "02.07.2021"
        second_date = "07.07.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.delete_task(login, password, project, column, name)
            status = False
        except EndBeforeStart:
            status = True

        self.assertEqual(status, True)

    def test_task_add_exist(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        name = "TestDate"
        desc = "TestDesc"
        first_date = "20.10.2019"
        second_date = "25.10.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.delete_task(login, password, project, column, name)
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, False)

    def test_task_add_no_user(self):
        login = "test1"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "20.10.2019"
        second_date = "25.10.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.delete_task(login, password, project, column, name)
            status = True
        except NoUser:
            status = False

        self.assertEqual(status, False)

    def test_task_incorrect_password(self):
        login = "test"
        password = "test1"
        project = "TestProject"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "20.10.2019"
        second_date = "25.10.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.delete_task(login, password, project, column, name)
            status = True
        except IncorrentPassword:
            status = False

        self.assertEqual(status, False)

    def test_task_edit_name(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "20.10.2019"
        second_date = "25.10.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.edit('name', login, password, project, column, name, "newtest")
            TaskController.delete_task(login, password, project, column, "newtest")
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, True)

    def test_task_edit_description(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "20.10.2019"
        second_date = "25.10.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.edit('desc', login, password, project, column, name, "newtest")
            TaskController.delete_task(login, password, project, column, name)
            status = True
        except Exception as err:
            print(err)
            status = False

        self.assertEqual(status, True)

    def test_task_edit_no_user_no_name(self):
        login = "test1"
        password = "test"
        project = "TestProject1"
        column = "TestColumn"
        name = "TestTask"
        desc = "TestDesc"
        first_date = "20.10.2019"
        second_date = "25.10.2020"
        tags = "first, second"
        priority = 5

        try:
            TaskController.add_task(login, password, project, column, name, desc, first_date, second_date, tags,
                                    priority)
            TaskController.edit('desc', login, password, project, column, name, "newtest")
            TaskController.delete_task(login, password, project, column, name)
            status = True
        except CannotGetProject:
            status = False

        self.assertEqual(status, False)


if __name__ == '__main__':
    unittest.main()
