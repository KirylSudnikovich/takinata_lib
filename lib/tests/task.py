import unittest
import datetime
from lib.controllers.task import TaskController


class TestsTask(unittest.TestCase):

    def test_task_add(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = 6
        name = "test task1"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2018"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except Exception as error:
            print(error)
            status = False
        self.assertEquals(status, True)

    def test_task_add_already_exist(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = 6
        name = "test task1"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2018"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_delete(self):
        try:
            TaskController.delete_task_by_name(6, "test task1")
            status = True
        except Exception as error:
            print(error)
            status = False
        self.assertEquals(status, True)

    def test_task_add_incorrect_password(self):
        login = "tester"
        password = "tester"
        project_id = 9
        category_id = 6
        name = "test task3"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2018"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_incorrect_project(self):
        login = "tester"
        password = "tester228"
        project_id = 1
        category_id = 6
        name = "test task4"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2018"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_noproject(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        category_id = 6
        name = "test task5"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2018"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_no_category_in_project(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = 25
        name = "test task6"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2018"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_no_category(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = -1
        name = "test task"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2018"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_end_before_start(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = -1
        name = "test task"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2017"
        end_time = "13:00"
        priority = "max"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_no_priority(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = -1
        name = "test task"
        desc = "task description"
        type = 1
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2017"
        end_time = "13:00"
        priority = "John Cena"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_no_type(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = -1
        name = "test task"
        desc = "task description"
        type = 3
        start_date = "10/08/2018"
        start_time = "10:00"
        end_date = "12/08/2017"
        end_time = "13:00"
        priority = "John Cena"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_incorrect_year(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = -1
        name = "test task"
        desc = "task description"
        type = 1
        start_date = "10/08/2015"
        start_time = "10:00"
        end_date = "12/08/2017"
        end_time = "13:00"
        priority = "John Cena"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_add_incorrect_login(self):
        login = "testerergb"
        password = "tester228"
        project_id = 9
        category_id = -1
        name = "test task"
        desc = "task description"
        type = 1
        start_date = "10/08/2015"
        start_time = "10:00"
        end_date = "12/08/2017"
        end_time = "13:00"
        priority = "John Cena"
        try:
            task = TaskController.add_task(login, password, project_id, category_id, name, desc, type, start_date,
                                           start_time,
                                           end_date, end_time, priority)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_get_all_users_tasks_incorrect_password(self):
        login = "tester"
        password = "no_tester"
        try:
            TaskController.get_all_users_task(login, password)
            status = True
        except:
            status = False
        self.assertEquals(status, False)


    def test_task_get_all_users_tasks_incorrect_username(self):
        login = "test3r"
        password = "tester228"
        try:
            TaskController.get_all_users_task(login, password)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_task_get_all_users_tasks(self):
        login = "tester"
        password = "tester228"
        try:
            TaskController.get_all_users_task(login, password)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_assosiated_task(self):
        login = "tester"
        password = "tester228"
        try:
            task = TaskController.get_task_by_id(16)
            TaskController.get_assosiated_task(login, password, task)
            status = True
        except Exception as er:
            print(er)
            status = False
        self.assertEquals(status, True)

    def test_get_assosiated_task_incorrect_id(self):
        login = "tester"
        password = "tester228"
        try:
            task = TaskController.get_task_by_id(-228)
            TaskController.get_assosiated_task(login, password, task)
            status = True
        except Exception as er:
            print(er)
            status = False
        self.assertEquals(status, False)

    def test_cancel_task(self):
        login = "tester"
        password = "tester228"
        try:
            task = TaskController.get_task_by_id(14)
            TaskController.cancel_task(task)
            status = True
        except :
            status = False
        self.assertEquals(status, True)

    def test_show_tasks(self):
        login = "tester"
        password = "tester228"
        try:
            TaskController.show_tasks(login, password, 6)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_show_tasks_no_username(self):
        login = "testerfrgbhng"
        password = "tester228"
        try:
            TaskController.show_tasks(login, password, 6)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_show_tasks_no_password(self):
        login = "tester"
        password = "tester228efrg"
        try:
            TaskController.show_tasks(login, password, 6)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_show_tasks_nocategory(self):
        login = "tester"
        password = "tester228"
        try:
            TaskController.show_tasks(login, password, 50)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_parent_task(self):
        login = "tester"
        password = "tester228"
        try:
            task = TaskController.get_task_by_id(1502)
            TaskController.get_parent_task(login, password, task)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_parent_task_no_parent(self):
        login = "tester"
        password = "tester228"
        try:
            task = TaskController.get_task_by_id(1501)
            TaskController.get_parent_task(login, password, task)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_parent_task_no_password(self):
        login = "tester"
        password = "tester2fe28"
        try:
            task = TaskController.get_task_by_id(1502)
            TaskController.get_parent_task(login, password, task)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_parent_task_no_username(self):
        login = "testeer"
        password = "tester228"
        try:
            task = TaskController.get_task_by_id(1501)
            TaskController.get_parent_task(login, password, task)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_check_notification(self):
        login = "tester"
        password = "tester228"
        try:
            TaskController.check_notifications(login, password)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_check_notification_no_user(self):
        login = "tefrgster"
        password = "tester228"
        try:
            TaskController.check_notifications(login, password)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_check_notification_no_passworf(self):
        login = "tester"
        password = "tesfvgbhter228"
        try:
            TaskController.check_notifications(login, password)
            status = True
        except:
            status = False
        self.assertEquals(status, False)