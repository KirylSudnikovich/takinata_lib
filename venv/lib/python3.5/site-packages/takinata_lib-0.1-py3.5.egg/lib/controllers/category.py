import os
import lib.logger as logger
from lib.exception import *
from lib.models.models import Category
from lib.controllers.user import UserController
from lib.storage.category import CategoryStorage
from lib.storage.project import ProjectStorage


class CategoryController:
    """
    The data handler for the category. Allows you to create, modify, show or return all prject categories and
    delete categories.

    """

    log_tag = "CategoryController"
    log = logger.get_logger(log_tag)

    @staticmethod
    def create_category(username, password, project_id, name, description):
        """
        Creates a category for the specified project with specified name and description
        :param username: who want create a new category
        :param password: user password
        :param project_id: id of the project where user want to create a category
        :param name: name of the category
        :param description: description of the category
        :return: None. Category will be created and store in database
        """
        user = UserController.get_user_by_name(username)
        if user.password == password:
            project = ProjectStorage.get_project_by_id(project_id)
            if ProjectStorage.is_admin(user.username, project_id):
                all_categories = CategoryStorage.get_all_categories(project)
                have = None
                for cat in all_categories:
                    if cat.name == name and cat.project_id == project_id:
                        have = True
                        CategoryController.log.info(
                            "Category {} can't created in {} because category with this name already exist in "
                            "{} project".format(name, username, project.name))
                        raise ColumnWithThisNameAlreadyExist
                if not have:
                    category = Category(name=name, desc=description, project_id=project.id)
                    CategoryStorage.add_category_to_db(category)
                    CategoryController.log.info(
                        "Category '{}' was successfully created by {}".format(name, username))
            else:
                CategoryController.log.error(
                    "User {} have not permission to create category in this project".format(username))
                raise NoPermission
        else:
            CategoryController.log.error("User {} has entered an incorrect password")
            raise WrongPassword

    @classmethod
    def delete_category(cls, username, password, project_id, name):
        """
        Removes a category with the specified name from the specified project
        :param username: name of user, whitch want to delete a column
        :param password: user password
        :param project_id: id of a project in whitch user want to delete a category
        :param name: name of caregory to delete
        :return: None. Category will be removed from database
        """
        user = UserController.get_user_by_name(username)
        if user.password == password:
            if ProjectStorage.is_admin(user.username, project_id):
                category = CategoryStorage.get_column(project_id, name)
                if category != None:
                    CategoryStorage.delete_category_from_db(category)
                    CategoryController.log.info("Category {} was successfully deleted by {}".format(name, username))
                else:
                    raise ThereIsNoSuchCategory
            else:
                CategoryController.log.error(
                    "User {} have not permission to create category in this project".format(username))
                raise NoPermission
        else:
            CategoryController.log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def edit_name_by_id(cls, username, password, project_id, category_id, new_name):
        """
        The change of name of the category
        :param username: username of project user
        :param password: password of user
        :param project_id: id of project where category is
        :param category_id: id of category
        :param new_name: new name of category
        :return: None. New name was saved in database
        """
        category = CategoryStorage.get_category_by_id(category_id)
        person = UserController.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project_by_id(project_id)
            if ProjectStorage.is_admin(person.username, project_id):
                categories = CategoryController.show_all(username, password, project)
                have = False
                for cat in categories:
                    if cat.name == new_name and cat.id != category_id:
                        have = True
                if not have:
                    category.name = new_name
                    CategoryStorage.save(category)
                    CategoryController.log.info("Category was successfully saved")
                else:
                    CategoryController.log.error("Category with this name is already exist")
                    raise ColumnWithThisNameAlreadyExist
            else:
                raise NoPermission
        else:
            CategoryController.log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def edit_desc_by_id(cls, username, password, project_id, category_id, new_desc):
        """
        Change the description of the project
        :param username: username of column creator
        :param password: password of creator
        :param project_id: project id of project where category is
        :param category_id: category id
        :param new_desc: new description of category
        :return: None. New description saved in database
        """
        category = CategoryStorage.get_category_by_id(category_id)
        person = UserController.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project_by_id(project_id)
            if ProjectStorage.is_admin(person.username, project.id):
                category.desc = new_desc
                CategoryStorage.save(category)
                CategoryController.log.info("Category was successfully saved")
            else:
                CategoryController.log.error(
                    "User {} have no permission to edit desc of {}".format(username, project.name))
                raise NoPermission
        else:
            CategoryController.log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def get_all_categories(cls, username, password, project):
        """
        Return all categories of project
        :param username: username of user executor
        :param password: user password
        :param project: project in which categories need to find
        :return:
        """
        user = UserController.get_user_by_name(username)
        if user.password == password:
            cats = CategoryStorage.get_all_categories(project)
            return cats
        else:
            CategoryController.log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def get_category_by_id(cls, id):
        """
        Return category with 'id' id
        :param id:
        :return: Category
        """
        category = CategoryStorage.get_category_by_id(id)
        if category != None:
            CategoryController.log.info("Category successfully returned")
            return category
        else:
            CategoryController.log.error("There is no category with that id ({})".format(id))
            raise ThereIsNoSuchCategory

    @classmethod
    def show_all(cls, username, password, project):
        """
        Displays all categories of the project
        :param username: user, which want to watch categories list in project
        :param password: user password
        :param project_id: the project id whose categories you want to show
        :return: List 'cats', that contain all categories of project 'project' or 'None' if there is no categories
        """
        if type(project) == int:
            project = ProjectStorage.get_project_by_id(project)
        user = UserController.get_user_by_name(username)
        if user.password == password:
            cats = CategoryStorage.get_all_categories(project)
            CategoryController.log.info("All categories for {} project was shown by {}".format(project.name, username))
            return cats
        else:
            CategoryController.log.error("Incorrect password for {}".format(username))
            raise WrongPassword
