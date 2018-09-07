import sqlite3

import lib.conf as conf
from lib.models.models import Category, Project
from lib.exception import *
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

engine = create_engine(conf.get_path_to_db())
from sqlalchemy.ext.declarative import declarative_base

Session = sessionmaker(bind=engine)
session = Session()


class CategoryStorage:
    """
    This class provides the interaction of objects of class Category with a database (write / read / modify).
    """
    @classmethod
    def add_category_to_db(cls, category):
        """
        Add the sent column to the database
        :param column: an instance of the Column type to be added to the database
        :return: None. Category was added to database
        """
        session.add(category)
        session.commit()
        session.close()

    @classmethod
    def save(self, category):
        """
        Saves all instance fields to the database
        :param column: the instance that you want to keep
        :return: None. Category was saved in database
        """
        new_category = session.query(Category).filter(Category.id == category.id).first()
        new_category.name = category.name
        new_category.desc = category.desc
        session.commit()
        session.close()

    @classmethod
    def delete_category_from_db(cls, category):
        """
        Remove the transferred instance from the database
        :param category: the instance you want to delete
        :return: None. Category was deleted from database
        """
        session.delete(category)
        session.commit()
        session.close()

    @classmethod
    def get_column(cls, project_id, name):
        """
        Get an instance of a class with the specified name
        :param project_name: the name of the project that contains the category
        :param name: the name of the category
        :return: Category with 'name' in 'project_id' project
        """
        category = session.query(Category).filter(Category.name == name and Category.project_id == project_id).first()
        session.close()
        return category

    @classmethod
    def get_category_by_id(cls, id):
        """
        Get an instance of a class with the specified name
        :param id: category id
        :return: Category with 'id' id
        """
        category = session.query(Category).filter(Category.id == id).first()
        session.close()
        return category

    @classmethod
    def get_all_categories(cls, project):
        """
        Get a list consisting of all columns included in the project
        :param project_id: the id of a project
        :return: all cols, that project exist
        """
        cats = []
        project = session.query(Project).filter(Project.id == project.id).first()
        categories = session.query(Category).filter(Category.project_id == project.id).all()
        categories = list(categories)
        session.close()
        if type(categories) == list:
            return categories
        elif categories is None:
            return []
        else:
            cats.append(categories)
            return cats