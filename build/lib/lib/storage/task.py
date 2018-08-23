import sqlite3
import lib.conf as conf
from lib.exception import *
from lib.models.models import Task, Project, Column
from lib.storage.category import *
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
engine = create_engine(conf.get_path_to_db())
from sqlalchemy.ext.declarative import declarative_base

class TaskStorage:
    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def add_task_to_db(cls, task):
        TaskStorage.session.add(task)
        TaskStorage.session.commit()
        TaskStorage.session.close()

    @classmethod
    def delete_task_from_db(cls, task):
        TaskStorage.session.delete(task)
        TaskStorage.session.commit()
        TaskStorage.session.close()

    @classmethod
    def send_to_archive(cls, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute(
            "UPDATE tasks SET archive=('%s') WHERE name==('%s') AND column_id==('%s')" % (1, task.name, task.column_id))
        conn.commit()
        conn.close()

    @classmethod
    def save(self, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE tasks SET name=('%s'),desc=('%s'),project_id=('%s'),column_id=('%s'),user_id=('%s'),"
                  "first_date=('%s'),second_date=('%s'), edit_date=('%s'), tags=('%s'),priority=('%s'),archive=('%s'),"
                  "is_subtask=('%s') WHERE id ==('%s')"
                  % (task.name, task.desc, task.project_id, task.column_id, task.user_id, task.first_date,
                     task.second_date, task.edit_date, task.tags, task.priority, task.archive, task.is_subtask, task.id))
        conn.commit()
        conn.close()

    @classmethod
    def get_task(cls, project_name, column_name, name):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        column = ColumnStorage.get_column(project_name, column_name)
        c.execute("SELECT * FROM tasks WHERE column_id==('%s') AND name==('%s')" % (column.id, name))
        data = c.fetchone()
        try:
            task = Task(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11],
                        data[12], data[0])
        except Exception:
            raise CannotGetProject
        return task

    @classmethod
    def get_all_tasks(cls, project_id, category_id):
        taskz = []
        project = ProjectStorage.get_project_by_id(project_id)
        column = ColumnStorage.get_column_by_id(project_id, category_id)
        tasks = TaskStorage.session.query(Task).filter(Task.category_id == category_id).all()
        TaskStorage.session.close()
        if type(tasks) == list:
            return tasks
        else:
            return taskz

    @classmethod
    def get_task_by_id(cls, id):
        """
        Get an instance of a class with the specified name
        :param project_name: the name of the project that contains the column
        :param name: the name of the column
        :return:
        """
        task = TaskStorage.session.query(Task).filter(Task.id == id).first()
        TaskStorage.session.close()
        return task

    @classmethod
    def get_all_subtasks(cls, project_name, column_name, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM task_subtask WHERE task_id == ('%s')"% task.id)
        data = c.fetchall()
        subtask_list = []
        for i in data:
            task = TaskStorage.get_task_by_id(project_name, column_name, i[0])
            subtask_list.append(task)
        return subtask_list

    @classmethod
    def set_subtask(cls, task1, task2):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("INSERT INTO task_subtask (subtask_id, task_id) VALUES ('%s','%s')" % (task1.id, task2.id))
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        """

        :return:
        """
        path = conf.get_path_to_db()
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("CREATE TABLE 'tasks' (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name`	TEXT, `desc` TEXT, "
                  "`project_id`	TEXT, `column_id` TEXT, `user_id` TEXT, `first_date` TEXT, `second_date` TEXT, "
                  "`edit_date`	TEXT, `tags` TEXT, `priority` TEXT, `archive` TEXT, `is_subtask` TEXT)")
        c.execute("CREATE TABLE 'task_subtask' (`subtask_id` TEXT, `task_id` TEXT )")
        conn.commit()
        conn.close()
