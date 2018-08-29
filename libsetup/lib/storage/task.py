import lib.conf as conf
from lib.exception import *
from lib.models.models import Task, Project, Column
from lib.storage.category import CategoryStorage
from lib.storage.project import ProjectStorage
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

engine = create_engine(conf.get_path_to_db())
Session = sessionmaker(bind=engine)
session = Session()

class TaskStorage:

    @classmethod
    def add_task_to_db(cls, task):
        """
        Add task to database
        :param task: task to add
        :return: None. Changes in database
        """
        session.add(task)
        session.commit()
        session.close()

    @classmethod
    def delete_task_from_db(cls, task):
        """
        Delete task from database
        :param task: task to delete
        :return: None. All changes in database
        """
        session.delete(task)
        session.commit()
        session.close()

    @classmethod
    def get_all_tasks(cls, category_id):
        """
        Return all tasks from the category
        :param category_id: category in which we are try to find tasks
        :return: list of 'task' which contain all tasks in category with id 'category_id'
        """
        taskz = []
        column = CategoryStorage.get_category_by_id(category_id)
        tasks = session.query(Task).filter(Task.category_id == category_id).all()
        session.close()
        if type(tasks) == list:
            return tasks
        else:
            taskz.append(tasks)
            return taskz

    @classmethod
    def get_all_user_task(cls, user):
        """
        Return all tasks in which use
        :param user: user which need to get all him tasks
        :return: List of 'task' of None depends of user task count
        """
        tasks = session.query(Task).filter(Task.user_id == user.id).all()
        session.close()
        return tasks

    @classmethod
    def get_task_by_id(cls, id):
        """
        Return task with the specified id
        :param id: task_id to find
        :return: 'task' of None if task with 'id' no in database
        """
        task = session.query(Task).filter(Task.id == id).first()
        session.close()
        return task

    @classmethod
    def get_all_subtasks(cls, task):
        """
        Return all subtask for task
        :param task: task for which we are try to find subtask
        :return: List of 'task' that is subtask for sended task or None if there is no one
        """
        task_list = session.query(Task).filter(Task.parent_task_id == task.id).all()
        session.close()
        return task_list

    @classmethod
    def cancel_task(cls, task):
        """
        Set status to 'Done' for the task
        :param task: task to cancel
        :return: None. All changes in database
        """
        task_save = session.query(Task).filter(Task.id == task.id).first()
        task_save.is_archive = 1
        session.commit()
        session.close()

    @classmethod
    def refresh_task_date(cls, task):
        """
        Refresh task_date after regular task reload
        :param task: task to refresh
        :return: None. All changes in database
        """
        task_save = session.query(Task).filter(Task.id == task.id).first()
        task_save.start_date = task.start_date
        task_save.end_date = task.end_date
        session.commit()
        session.close()

    @classmethod
    def save_as_parent(cls, task):
        """
        Set tast as parent
        :param task: task to set as parent
        :return: None. All changes in database
        """
        task_save = session.query(Task).filter(Task.id == task.id).first()
        task_save.is_parent = task.is_parent
        session.commit()
        session.close()

    @classmethod
    def save_subtask(cls, task):
        """
        Set task as subtask
        :param task: task to set
        :return: None. All changes in database
        """
        task_save = session.query(Task).filter(Task.id == task.id).first()
        task_save.is_subtask = 1
        task_save.parent_task_id = task.parent_task_id
        session.commit()
        session.close()

    @classmethod
    def save_assosiate(cls, task):
        """
        Save assosiate for the task
        :param task: task to save assosiate
        :return: None. All changes in database
        """
        task_save = session.query(Task).filter(Task.id == task.id).first()
        task_save.assosiated_task_id = task.assosiated_task_id
        session.commit()
        session.close()

    @classmethod
    def get_parent_task(cls, task):
        """
        Return parent task for task
        :param task: task for which we are try to find parent task
        :return: parent task for sended task or none if there is no one
        """
        parent_task = session.query(Task).filter(Task.id == task.parent_task_id).first()
        session.close()
        return parent_task

    @classmethod
    def get_last_task(cls):
        """
        Return last task from database
        :return: task with max id
        """
        task = session.query(Task).order_by(Task.id.desc()).first()
        session.close()
        return task

    @classmethod
    def delete_task_by_name(cls, category_id, name):
        """
        Delete task with specified name
        :param category_id: category in which user want to delete task
        :param name: task name
        :return: None. Task was deleted from database
        """
        task = session.query(Task).filter(Task.category_id == category_id and Task.name == name).first()
        session.delete(task)
        session.commit()
        session.close()