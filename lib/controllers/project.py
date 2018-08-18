import lib.logger as logger
import os
from lib.exception import *
from lib.models.user import Project
from lib.storage.project import ProjectStorage
from lib.storage.user import UserStorage
import lib.conf as conf

class ProjectController:
    log_tag = "ProjectController"

    @classmethod
    def create(cls, username, password, name, description):
        """
        Create a project with a specified name and description
        :param username: user, who want to create a new project
        :param password: user password
        :param name: name of new project
        :param description: description of new project
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            project = Project(name=name, description=description, user_id=user.id)
            project.users.append(user)
            ProjectStorage.add_project_to_db(project, user)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword


    @classmethod
    def delete(cls, username, password, name):
        """
        Deletes the project with the specified name
        :param username: user, creator of project
        :param password: user password
        :param name: name of project to delete
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            project = ProjectStorage.get_project(name)
            ProjectStorage.check_permission(user, project)
            guys = ProjectStorage.get_all_persons_in_project(project)
            for i in guys:
                ProjectController.su_delete_person_from_project(username, password, i, project.name)
            ProjectStorage.delete_with_object(project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def add_person_to_project(cls, username, password, project, person):
        """
        Adds an artist to the project
        :param username: name of project creator
        :param password: creator password
        :param person: the name of the user you want to add to the project
        :param project: project name
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        admin = UserStorage.get_user_by_name(username)
        if admin.password == password:
            if ProjectStorage.is_admin(admin, project) == 0:
                userlist = ProjectStorage.get_all_persons_in_project(project)
                have = False
                for i in userlist:
                    if i == person.id:
                        have = True
                if not have:
                    ProjectStorage.add_person_to_project(person, project)
                else:
                    log.error("User {} is already exist in this project".format(username))
                    raise UserAlreadyExistInProject
            else:
                log.error("You are not the Creator of the project")
                raise UAreNotAdmin
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def delete_person_from_project(cls, username, password, project, person):
        """
        The removal of the contractor from the project
        :param username: username of creator
        :param password: creator password
        :param person: person to delete
        :param project: project name
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        admin = UserStorage.get_user_by_name(username)
        if admin.password == password:
            if ProjectStorage.is_admin(admin, project) == 0:
                guys = ProjectStorage.get_all_persons_in_project(project)
                have = False
                if guys[0][0] == person.id:
                    log.error("User was tried to delete a creator of the project")
                    raise CannotDeleteCreator
                for i in range(len(guys)):
                    if guys[i][0] == person.id:
                        have = True
                if not have:
                    log.error("User is not exist")
                    raise UserIsNotExistInProject
                else:
                    ProjectStorage.delete_person_from_project(person, project)
            else:
                log.error("You are not the Creator of the project")
                raise UAreNotAdmin
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def su_delete_person_from_project(cls, username, password, person, project):
        """
        Delete all the workers from the project, you can also delete the project Creator
        :param username: name of creator
        :param password: creator password
        :param person: person to delete
        :param project: project name
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        project = ProjectStorage.get_project(project)
        admin = UserStorage.get_user_by_name(username)
        person = UserStorage.get_user_by_id(person)
        if admin.password == password:
            ProjectStorage.is_admin(admin, project)
            guys = ProjectStorage.get_all_persons_in_project(project)
            have = False
            for i in range(len(guys)):
                if guys[i][0] == person.user_id:
                    have = True
            if not have:
                log.error("User is not exist")
                raise UserIsNotExistInProject
            else:
                ProjectStorage.delete_person_from_project(person, project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def show_all(cls, username, password):
        """
        Displays a list of all projects with the participants of these projects
        :param username:
        :param password:
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        user = UserStorage.get_user_by_name(username)
        new_list = []
        if user.password == password:
            project_list = ProjectStorage.show_all()
            print(project_list)
            for i in project_list:
                have = False
                guys = ProjectStorage.get_all_persons_in_project_by_id(i)
                for j in guys:
                    print(j.id)
                    if user.id == j.id:
                        have = True
                if have:
                    new_list.append(i)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword
        return new_list

    @classmethod
    def edit_name(cls, username, password, project_name, new_name):
        """
        Editing the project name
        :param username: name of project creator
        :param password: creator password
        :param project_name: name of the project to be changed
        :param new_name: new name of project
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        person = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        print(project_name)
        if person.password == password:
            ProjectStorage.is_admin(person, project)
            project.name = new_name
            ProjectStorage.save(project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def edit_description(cls, username, password, project_name, new_desc):
        """
        Editing the project description
        :param username: name of project creator
        :param password: creator password
        :param project_name: name of the project to be changed
        :param new_desc: new description of project
        :return:
        """
        log = logger.get_logger(ProjectController.log_tag)
        person = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if person.password == password:
            ProjectStorage.is_admin(person, project)
            project.description = new_desc
            ProjectStorage.save(project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword
