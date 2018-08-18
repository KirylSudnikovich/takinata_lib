import os

from lib.controllers.project import ProjectController
from lib.controllers.regular_task import RegularTaskController
from lib.controllers.task import TaskController
from lib.controllers.user import UserController
from lib.controllers.column import ColumnController


def check_tracker_folder(path):
    """
    Checks for a directory at the specified path. If the directory does not exist, it will be created
    :param path: path to check
    :return:

    """
    if not os.path.exists(path):
        f = open(path, 'w')
        f.close()
        print("all clear")
        return 1


def check_db_exists(path):
    """
    Checks if the database exists in the specified directory. If not - creates this base
    :param path: path to database
    :return:
    """
    if check_tracker_folder(path) == 1:
        print("погнали")
        TaskController.create_table()
        RegularTaskController.create_table()
        UserController.create_table()
        ProjectController.create_table()
        ColumnController.create_table()
        return 0
