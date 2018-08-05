import unittest

from Tracker.lib.controllers.Column import *
from Tracker.lib.Exception import *


class TestsColumn(unittest.TestCase):

    def test_column_create(self):
        login = "test"
        password = "test"
        name = "TestProject"
        c_name = "column_name"
        c_desc = "column_description"

        try:
            ColumnController.create_columm(login, password, name, c_name, c_desc)
            ColumnController.delete_column(login, password, name, c_name)
            status = True
        except:
            status = False

        self.assertEqual(status, True)

    def test_column_create_error(self):
        login = "test"
        password = "test"
        name = "TestProject"
        c_name = "TestColumn"
        c_desc = ""

        try:
            ColumnController.create_columm(login, password, name, c_name, c_desc)
            status = True
        except ColumnWithThisNameAlreadyExist:
            status = False

        self.assertEqual(status, False)

    def test_column_delete(self):
        login = "test"
        password = "test"
        name = "TestProject"
        c_name = "column_name"
        c_desc = "column_description"

        try:
            ColumnController.create_columm(login, password, name, c_name, c_desc)
            ColumnController.delete_column(login, password, name, c_name)
            status = True
        except:
            status = False

        self.assertEqual(status, True)

    def test_column_show(self):
        login = "test"
        password = "test"
        name = "TestProject"
        c_name = "column_name"
        c_desc = "column_description"

        try:
            ColumnController.create_columm(login, password, name, c_name, c_desc)
            ColumnController.show_all(login, password, name)
            ColumnController.delete_column(login, password, name, c_name)
            status = True
        except:
            status = False

        self.assertEqual(status, True)

    def test_column_edit(self):
        login = "test"
        password = "test"
        project = "TestProject"
        column = "TestColumn"

        try:
            ColumnController.edit_desc(login, password, project, column, "test")
            status = True
        except:
            status = False

        self.assertEqual(status, True)


if __name__ == '__main__':
    unittest.main()
