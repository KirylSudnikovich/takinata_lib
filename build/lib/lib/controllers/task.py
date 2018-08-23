from datetime import *

from lib.exception import *
from lib.models.models import Task
from lib.storage.category import *
from lib.storage.project import *
from lib.storage.task import *
from lib.storage.user import *
import lib.logger as logger


class TaskController:
    log_tag = "TaskController"

    @classmethod
    def add_task(cls, username, password, project_id, column_id, name, desc, start_date, start_time, end_date, end_time, tags,
                 priority):
        """
        Creates a task in the selected column of the selected project with the specified time frame, tags, and priority
        tasks
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param name:
        :param desc:
        :param first_date:
        :param second_date:
        :param tags:
        :param priority:
        :return:
        """
        log = logger.get_logger(TaskController.log_tag)
        project = ProjectStorage.get_project_by_id(project_id)
        column = ColumnStorage.get_column_by_id(project_id, column_id)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            # try:
            start = datetime.strptime(start_date, '%m/%d/%Y')
            end = datetime.strptime(end_date, '%m/%d/%Y')
            if end < start:
                log.error("EndDate is before StartDate")
                raise EndBeforeStart
            # except Exception:
            # raise NotDate
            ProjectStorage.check_permission(user, project)
            task_names = TaskStorage.get_all_tasks(project_id, column_id)
            have = False
            for i in task_names:
                if i.name == name:
                    have = True
            if not have:
                task = Task(name=name,desc=desc,start_date=start_date, start_time=start_time, end_date=end_date,
                            end_time=end_time, tags=tags, priority=priority, is_archive=0, is_subtask=0, user_id=user.id,
                            category_id=column.id, project_id=project.id)
                TaskStorage.add_task_to_db(task)
                return task
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
        log = logger.get_logger(TaskController.log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            ProjectStorage.is_admin(user, project)
            try:
                task = TaskStorage.get_task(project_name, column_name, task_name)
            except Exception:
                log.error("There is no task with this name")
                raise NoTask
            if task.archive == '1':
                log.error("Task is already in archive")
                raise AlreadyInArchive
            else:
                if task.is_subtask == 1:
                    TaskStorage.delete_task_from_db(task)
                else:
                    list = TaskStorage.get_all_subtasks(project_name, column_name, task)
                    can = True
                    for i in list:
                        if i.archive != '1':
                            can = False
                    if can:
                        TaskStorage.delete_task_from_db(task)
                    else:
                        log.eror("Can not to delete task, because task have some subtask")
                        raise CanNotDeleteBecauseSubtasks
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def show_tasks(cls, username, password, project_id, column_id):
        """
        Shows tasks for the specified column
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :return:
        """
        log = logger.get_logger(TaskController.log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project_by_id(project_id)
        column = ColumnStorage.get_column_by_id(project_id, column_id)
        if user.password == password:
            ProjectStorage.check_permission(user, project)
            tasks = TaskStorage.get_all_tasks(project_id, column_id)
            return tasks
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def set_subtask(cls, username, password, project_name, column_name, task1, task2):
        """
        Make task 1 a subtask of task 2
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param task1:
        :param task2:
        :return:
        """
        log = logger.get_logger(TaskController.log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            ProjectStorage.check_permission(user, project)
            task1 = TaskStorage.get_task(project_name, column_name, task1)
            task2 = TaskStorage.get_task(project_name, column_name, task2)
            if task1.is_subtask == '0':
                if task1.first_date > task2.first_date and task1.second_date < task2.second_date:
                    if task1.priority > task2.priority:
                        raise SubtaskPriorityException
                    else:
                        tasks = TaskStorage.get_all_subtasks(project_name, column_name, task2)
                        can = True
                        for i in tasks:
                            if task1 in tasks:
                                can = False
                        if can:
                            TaskStorage.set_subtask(task1, task2)
                            task1.is_subtask = 1
                            TaskStorage.save(task1)
                        else:
                            log.error("This task is already subtask")
                            raise AlreadySubtask
                else:
                    log.error("Subtask date error")
                    raise SubtaskDateException
            else:
                log.error("Task is already subtask")
                raise AlreadySubtask
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def edit(cls, type_of_edit, username, password, project_name, column_name, task_name, new_value):
        """
        Editing an attribute for a specified task
        :param type_of_edit:
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param task_name:
        :param new_value:
        :return:
        """
        log = logger.get_logger(TaskController.log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        task = TaskStorage.get_task(project_name, column_name, task_name)
        if user.password == password:
            ProjectStorage.check_permission(user, project)
            if type_of_edit == 'name':
                task.name = new_value
            elif type_of_edit == 'description' or 'desc':
                task.desc = new_value
            elif type_of_edit == 'tags':
                task.tags = new_value
            elif type_of_edit == 'priority':
                try:
                    task.priority = int(new_value)
                except:
                    log.error("Type error")
                    raise TypeErro
            TaskStorage.save(task)
        else:
            raise WrongPassword

    @classmethod
    def create_table(cls):
        TaskStorage.create_table()