import lib.logger as logger

from datetime import *
from lib.storage.project import *
from lib.storage.column import *
from lib.storage.regular_task import *
from lib.storage.user import *
from lib.models.regular_task import *


class RegularTaskController:
    log_tag = "RegularTaskController"

    @classmethod
    def add_task(cls, username, password, project_name, column_name, name, desc, first_date, second_date, step,
                 type_of_step, tags, priority):
        """
        Creates a regular task in the selected column of the selected project with the specified transition step and
        the specified times- by borders
        :param username: The name of the user who creates the task
        :param password: User password
        :param project_name: Project name where the task will be created
        :param column_name: Name of the column where the task will be created
        :param name: Task name
        :param desc: Task description
        :param first_date: The start date of task execution
        :param second_date: Task end date
        :param step: Step length
        :param type_of_step: Kind of step (minute/hour/day/month)
        :param edit_date: Date of last task editing
        :param tags: Tags
        :param priority: Task priority
        :return:
        """
        print("Здаров епта")
        log = logger.get_logger(RegularTaskController.log_tag)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        user = UserStorage.get_user_by_name(username)
        steps = ['day', 'week', 'month', 'year']
        if user.password == password:
            start = datetime.strptime(first_date, "%d.%m.%Y")
            end = datetime.strptime(second_date, "%d.%m.%Y")
            today = datetime.today()
            if start < today:
                log.error("Start date is before today")
                raise StartBeforeToday
            if end < today:
                log.error("End date is before today")
                raise EndBeforeToday
            if end < start:
                log.error("EndDate is before Start date")
                raise EndBeforeStart
            if type_of_step not in steps:
                log.error("Incorrect type of step")
                raise IncorrectTypeOfStep
            try:
                priority = int(priority)
                if priority <= 0 or priority > 10:
                    raise IncorrectPriority
            except Exception as err:
                log.error(err)
                raise ItsNotANumber
            ProjectStorage.check_permission(user, project)
            task_names = RegularTaskStorage.get_all_tasks(project_name, column_name)
            have = False
            for i in task_names:
                if i.name == name:
                    have = True
            if not have:
                regular_task = RegularTask(name, desc, project.id, column.id, user.user_id, first_date, second_date,
                                           step, type_of_step, tags, priority, 0, 0, str(date.today()))
                RegularTaskStorage.add_task_to_db(regular_task)
                return regular_task
            else:
                log.error("Task with this name is already exist")
                raise TaskWithThisNameAlreadyExist(name)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def delete_task(cls, username, password, project_name, column_name, task_name):
        """
        Delete the specified task
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param task_name:
        :return:
        """
        log = logger.get_logger(RegularTaskController.log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            ProjectStorage.is_admin(user, project)
            try:
                task = RegularTaskStorage.get_task(project_name, column_name, task_name)
            except Exception:
                log.error("There is no task with this name")
                raise NoTask
            RegularTaskStorage.delete_task_from_db(task)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def show_tasks(cls, username, password, project_name, column_name, key=None):
        """
        Shows tasks for the specified column
        :param key:
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :return:
        """
        log = logger.get_logger(RegularTaskController.log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        if user.password == password:
            ProjectStorage.check_permission(user, project)
            tasks = RegularTaskStorage.get_all_tasks(project_name, column_name, key)
            return tasks
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def re_create(cls, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        log = logger.get_logger(RegularTaskController.log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            tasks = RegularTaskStorage.get_all_tasks_for_user(user)
            for task in tasks:
                start_date = datetime.strptime(task.first_date, "%d.%m.%Y")
                end_date = datetime.strptime(task.second_date, "%d.%m.%Y")
                if end_date < datetime.today():
                    if task.type_of_step == 'day':
                        need = int(task.step)
                        x = end_date - start_date
                        print(x)
                        if x.days >= need:
                            print("Пересоздаём")
                            new_start = date.today()
                            task.first_date = new_start
                            RegularTaskStorage.save(task)
                            print("Задача пересоздана и сохранена")
                    #print("Type - {}, X = {}".format(type(x),x))
            return tasks
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def create_table(cls):
        RegularTaskStorage.create_table()


    @classmethod
    def next_date(cls, task):
        pass

    @classmethod
    def get_step(cls, task):
        num = task.step
        if task.type_of_step == 'day':
            return int(num)
        elif task.type_of_step == 'week':
            return int(num) * 7
        elif task.type_of_step == 'month':
            pass
