import sqlite3
import lib.conf as conf

from lib.exception import *
from lib.models.project import *
from lib.models.user import *


class ProjectStorage:
    @classmethod
    def add_project_to_db(cls, project, user):
        """
        Add an instance of the Project class to the database
        :param project: the instance of the Project class that you want to add
        :param user: an instance of the User class that is the Creator of the project
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT name, user_id FROM projects")
        all_projectnames = c.fetchall()
        yep = False
        for i in all_projectnames:
            if project.name == i[0] and user.user_id == i[1]:
                yep = True
        if not yep:
            c.execute("INSERT INTO projects (name, description, user_id) VALUES ('%s', '%s', '%s')" % (project.name,
                                                                                                       project.description,
                                                                                                       user.user_id))
            conn.commit()
            c.execute("SELECT id FROM projects WHERE name==('%s')" % project.name)
            id = c.fetchone()
            c.execute("INSERT INTO user_project (user_id, project_id) VALUES ('%d', '%d')" % (user.user_id, id[0]))
            conn.commit()
            conn.close()
        else:
            raise ProjectWithThisNameAlreadyExist()

    @classmethod
    def get_all_persons_in_project(cls, project):
        """
        Get the id of all users involved in the project
        :param project: the name of the project
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT user_id FROM user_project WHERE project_id ==('%s')" % project.id)
        data = c.fetchall()
        return data

    @classmethod
    def get_all_projects(cls, user_id):
        """
        Get a list of projects where the user with the specified id is the creator
        :param user_id: id of user
        :return:
        """
        projects = []
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE user_id ==('%s')" % user_id)
        data = c.fetchall()
        for i in data:
            project = Project(i[1],i[2],i[3],None,i[0])
            projects.append(project)
        return projects

    @classmethod
    def add_person_to_project(cls, person, project):
        """
        Adds the specified user to the project if the command was executed on behalf of the project creator
        :param person: person to add to the project
        :param project: project where you want to add the user
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("INSERT INTO user_project (user_id, project_id) VALUES ('%d','%d')"%(person.user_id,project.id))
        conn.commit()
        conn.close()

    @classmethod
    def delete_person_from_project(cls, person, project):
        """
        Remove the specified user from the project
        :param person: person to remove
        :param project: project where you want to remove the user
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM user_project WHERE user_id ==('%s') AND project_id==('%s')"% (person.user_id, project.id))
        conn.commit()
        conn.close()

    @classmethod
    def delete_with_object(cls, project):
        """
        Delete the specified project that was passed in the arguments
        :param project: project whitch you want to delete
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM projects WHERE name=('%s')" % project.name)
        conn.commit()
        conn.close()

    @classmethod
    def get_project(cls, name):
        """
        Getting the project with the specified name from the database
        :param name: name of the project
        :return: project
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE name==('%s')" % name)
        project_info = c.fetchone()
        try:
            project = Project(project_info[1], project_info[2], project_info[3], None, project_info[0])
            conn.close()
            return project
        except:
            conn.close()
            raise CannotGetProject

    @classmethod
    def show_all(cls):
        """
        Displays a list of all projects in which the specified user is involved
        :return: project list
        """
        project_list = []
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT name, description, user_id, id FROM projects")
        data = c.fetchall()
        for i in range(len(data)):
            c.execute("SELECT user_id FROM user_project WHERE project_id==('%d')" % data[i][3])
            project_users = c.fetchall()
            users_to_add = []
            for j in project_users:
                c.execute("SELECT * FROM users WHERE id==('%d')" % j[0])
                user_data = c.fetchone()
                user = User(user_data[1], user_data[2], user_data[3], user_data[0])
                users_to_add.append(user)
            project = Project(data[i][0], data[i][1], data[i][2], users_to_add)
            project_list.append(project)
        return project_list

    @classmethod
    def check_permission(cls, person, project):
        """
        Checks whether the specified user is participating in the project
        :param person: the supposed worker
        :param project: project to check
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        guys = ProjectStorage.get_all_persons_in_project(project)
        for i in guys:
            if i[0] == person.user_id:
                return
        raise NoPermission

    @classmethod
    def is_admin(cls, person, project):
        """
        Checks whether the specified user is the creator of the project
        :param person: the supposed creator
        :param project: project to check
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        guys = ProjectStorage.get_all_persons_in_project(project)
        if guys[0][0] == person.user_id:
            pass
        else:
            raise UAreNotAdmin

    @classmethod
    def save(self, project):
        """
        Saves the transferred instance of the Project class to the database
        :param project: project to save
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute(
            "UPDATE projects SET name=('%s'),description=('%s') WHERE id==('%d')" % (project.name, project.description,
                                                                                     project.id))
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        path = conf.get_path_to_db()
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("CREATE TABLE `projects` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name`	TEXT, `description`	TEXT, "
                  "`user_id`	INTEGER)")
        c.execute("CREATE TABLE `user_project` (`user_id` INTEGER, `project_id`	INTEGER )")
        conn.commit()
        conn.close()