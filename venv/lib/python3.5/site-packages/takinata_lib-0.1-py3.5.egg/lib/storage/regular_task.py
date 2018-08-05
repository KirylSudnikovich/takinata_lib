import sqlite3

import lib.conf as conf
from lib.models.regular_task import *
from lib.storage.column import *
from lib.storage.project import *
from lib.controllers.regular_task import *


def by_name_key(task):
    return task.name


def by_startdate_key(task):
    return task.first_date


def by_enddate_key(task):
    return task.second_date


def by_priority_key(task):
    return task.priority


class RegularTaskStorage:
    @classmethod
    def add_task_to_db(cls, task):
        """
        Добавление регулярной задачи в БД
        :param task:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute(
            "INSERT INTO regular_task (name, desc, project_id, column_id, user_id, first_date, second_date, step, "
            "type_of_step, edit_date, tags, priority, archive) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s',"
            "'%s', "
            "'%s','%s', '%s')" % (task.name, task.desc, task.project_id, task.column_id, task.user_id,
                                  task.first_date, task.second_date, task.step, task.type_of_step, task.edit_date,
                                  task.tags,
                                  task.priority, 0))
        conn.commit()
        conn.close()

    @classmethod
    def get_all_tasks(cls, project_name, column_name, key=None):
        """
        Получение списка всех регулярных задач для указанной колонки
        :param key:
        :param project_name:
        :param column_name:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        print("CHECK THIS ", column_name)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        c.execute("SELECT * FROM regular_task WHERE project_id==('%s') AND column_id==('%s')" % (project.id, column.id))
        data = c.fetchall()
        task_list = []
        for i in data:
            task = RegularTask(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[0])
            task_list.append(task)
        conn.close()
        if key:
            if key == 'name':
                task_list = sorted(task_list, key=by_name_key)
            elif key == 'priority':
                task_list = sorted(task_list, key=by_priority_key)
            elif key == 'start date':
                task_list = sorted(task_list, key=by_startdate_key)
            elif key == 'end date':
                task_list = sorted(task_list, key=by_enddate_key)
            else:
                raise ThisFeatureDoesNotExist
        else:
            pass
        return task_list

    @classmethod
    def get_all_tasks_for_user(cls, user):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM regular_task WHERE user_id==('%s')" % user.user_id)
        data = c.fetchall()
        task_list = []
        conn.close()
        for i in data:
            task = RegularTask(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[0])
            task_list.append(task)
        return task_list

    @classmethod
    def delete_task_from_db(cls, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM regular_task WHERE id==('%s')" % task.id)
        conn.commit()
        conn.close()

    @classmethod
    def save(self, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE regular_task SET name=('%s'),desc=('%s'),project_id=('%s'),column_id=('%s'),user_id=('%s'),"
                  "first_date=('%s'),second_date=('%s'), step=('%s'), type_of_step=('%s'), edit_date=('%s'), tags=('%s')"
                  ",priority=('%s'),archive=('%s') WHERE id ==('%s')"
                  % (task.name, task.desc, task.project_id, task.column_id, task.user_id, task.first_date,
                     task.second_date, task.step, task.type_of_step, task.edit_date, task.tags, task.priority,
                     task.archive, task.id))
        conn.commit()
        conn.close()

    @classmethod
    def get_task(cls, project_name, column_name, name):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        column = ColumnStorage.get_column(project_name, column_name)
        c.execute("SELECT * FROM regular_task WHERE column_id==('%s') AND name==('%s')" % (column.id, name))
        data = c.fetchone()
        try:
            task = RegularTask(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                               data[10],
                               data[11], data[12], data[0])
        except Exception:
            raise CannotGetProject
        return task

    @classmethod
    def create_table(cls):
        path = conf.get_path_to_db()
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("CREATE TABLE 'regular_task' (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name`	TEXT, `desc` TEXT, "
                  "`project_id`	TEXT, `column_id` TEXT, `user_id` TEXT, `first_date` TEXT, `second_date` TEXT, "
                  "`step` TEXT, `type_of_step` INTEGER, `edit_date`	TEXT, `tags` TEXT, `priority` TEXT, `archive` TEXT "
                  ")")
        conn.commit()
        conn.close()
